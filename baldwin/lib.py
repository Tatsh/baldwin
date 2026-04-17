"""Baldwin library."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from importlib import resources
from itertools import chain
from pathlib import Path
from shlex import quote
from shutil import which
from typing import TYPE_CHECKING, Literal, cast
import asyncio
import logging
import os
import subprocess as sp

from binaryornot.check import is_binary
from git import Actor, Repo
import anyio
import platformdirs
import tomlkit

if TYPE_CHECKING:
    from collections.abc import Iterable

    from .typing import BaldwinConfigContainer

__all__ = ('RepoInfo', 'auto_commit', 'format_', 'get_config', 'get_git_path', 'get_repo', 'git',
           'init', 'install_units', 'repo_info', 'set_git_env_vars')

log = logging.getLogger(__name__)

_MAX_PARALLEL_PRETTIER = max(1, (os.cpu_count() or 1))
"""Upper bound on concurrent Prettier invocations.

:meta hide-value:
"""


def git(args: Iterable[str]) -> None:
    """
    Front-end to git with git-dir and work-tree passed.

    Parameters
    ----------
    args : Iterable[str]
        Arguments to pass to ``git`` after the ``--git-dir`` and ``--work-tree`` options.
    """
    # Pass these arguments because of the hgit shortcut
    cmd = ('git', f'--git-dir={get_git_path()}', f'--work-tree={Path.home()}', *args)
    log.debug('Running: %s', ' '.join(quote(x) for x in cmd))
    sp.run(cmd, check=False)  # do not use env= because env vars controlling colour will be lost


def init() -> None:
    """
    Start tracking a home directory.

    Does nothing if the Git directory already exists.
    """
    if (git_path := get_git_path()).exists():
        return
    repo = Repo.init(git_path, expand_vars=False)
    repo.git.execute(('git', 'config', 'commit.gpgsign', 'false'))
    gitattributes = Path.home() / '.gitattributes'
    gitattributes.write_text(resources.read_text('baldwin.resources', 'default_gitattributes.txt'))
    gitignore = Path.home() / '.gitignore'
    gitignore.write_text(resources.read_text('baldwin.resources', 'default_gitignore.txt'))
    repo.index.add([gitattributes, gitignore])
    if jq := which('jq'):
        repo.git.execute(('git', 'config', 'diff.json.textconv', f'"{jq}" -MS .'))
        repo.git.execute(('git', 'config', 'diff.json.cachetextconv', 'true'))
    if (prettier := which('prettier')):
        node_modules_path = (Path(prettier).resolve(strict=True).parent / '..' /
                             '..').resolve(strict=True)
        if (node_modules_path / '@prettier/plugin-xml/src/plugin.js').exists():
            repo.git.execute((
                'git', 'config', 'diff.xml.textconv',
                f'"{prettier}" --no-editorconfig --parser xml --xml-whitespace-sensitivity ignore'))
            repo.git.execute(('git', 'config', 'diff.xml.cachetextconv', 'true'))
        repo.git.execute(('git', 'config', 'diff.yaml.textconv',
                          f'"{prettier}" --no-editorconfig --parser yaml'))
        repo.git.execute(('git', 'config', 'diff.yaml.cachetextconv', 'true'))


async def _can_open(file: anyio.Path) -> bool:
    """
    Check whether a file can be opened for reading.

    Parameters
    ----------
    file : anyio.Path
        Path to the file.

    Returns
    -------
    bool
        ``True`` if the file can be opened for reading, ``False`` otherwise.
    """
    try:
        handle = await file.open('rb')
    except OSError:
        return False
    await handle.aclose()
    return True


async def _classify_untracked(path: anyio.Path) -> anyio.Path | None:
    """
    Determine whether an untracked path should be staged.

    Runs :py:func:`_can_open` and :py:meth:`anyio.Path.is_file` concurrently, then defers to
    :py:func:`~binaryornot.check.is_binary` (in a worker thread) only when both succeed; the
    binary check reads the file and must not run on paths that cannot be opened or are not
    regular files.

    Parameters
    ----------
    path : anyio.Path
        Path to classify.

    Returns
    -------
    anyio.Path | None
        The input path when it should be staged, otherwise ``None``.
    """
    can_open, is_file = await asyncio.gather(_can_open(path), path.is_file())
    if not (can_open and is_file):
        return None
    if await asyncio.to_thread(is_binary, str(path)):
        return None
    return path


async def auto_commit() -> None:
    """Automated commit of changed and untracked files."""
    repo = get_repo()
    home = anyio.Path(Path.home())
    diff_items = [home / e.a_path for e in repo.index.diff(None) if e.a_path is not None]
    untracked = [home / y for y in repo.untracked_files]
    existing_results, untracked_results = await asyncio.gather(
        asyncio.gather(*(p.exists() for p in diff_items)),
        asyncio.gather(*(_classify_untracked(p) for p in untracked)))
    items_to_add = [
        *(Path(p) for p, exists in zip(diff_items, existing_results, strict=True) if exists),
        *(Path(p) for p in untracked_results if p is not None)
    ]
    items_to_remove = [
        Path(p) for p, exists in zip(diff_items, existing_results, strict=True) if not exists
    ]
    if items_to_add:
        await format_(items_to_add)
        repo.index.add(items_to_add)
    if items_to_remove:
        repo.index.remove(items_to_remove)
    if items_to_add or items_to_remove or len(repo.index.diff('HEAD')) > 0:
        repo.index.commit(f'Automatic commit @ {datetime.now(tz=timezone.utc).isoformat()}',
                          committer=Actor('Auto-committer', 'hgit@tat.sh'))


@dataclass
class RepoInfo:
    """General repository information."""
    git_dir_path: Path
    """Git directory."""
    work_tree_path: Path
    """Work tree."""


def repo_info() -> RepoInfo:
    """
    Get general repository information.

    Returns
    -------
    RepoInfo
        Paths to the Git directory and work tree.
    """
    return RepoInfo(git_dir_path=get_git_path(), work_tree_path=Path.home())


def install_units() -> None:
    """
    Install systemd units for automatic committing.

    Raises
    ------
    FileNotFoundError
        If the ``bw`` executable is not found in ``PATH``.
    """
    bw = which('bw')
    if not bw:
        raise FileNotFoundError
    service_file = Path('~/.config/systemd/user/home-vcs.service').expanduser()
    service_file.write_text(f"""[Unit]
Description=Home directory VCS commit

[Service]
Environment=NO_COLOR=1
ExecStart={bw} auto-commit
Type=oneshot
""")
    log.debug('Wrote to `%s`.', service_file)
    timer_file = Path('~/.config/systemd/user/home-vcs.timer').expanduser()
    timer_file.write_text("""[Unit]
Description=Hexahourly trigger for Home directory VCS

[Timer]
OnCalendar=0/6:0:00

[Install]
WantedBy=timers.target
""")
    log.debug('Wrote to `%s`.', timer_file)
    cmd: tuple[str, ...] = ('systemctl', '--user', 'enable', '--now', 'home-vcs.timer')
    log.debug('Running: %s', ' '.join(quote(x) for x in cmd))
    sp.run(cmd, check=True)
    cmd = ('systemctl', '--user', 'daemon-reload')
    log.debug('Running: %s', ' '.join(quote(x) for x in cmd))
    sp.run(cmd, check=True)


def get_git_path() -> Path:
    """
    Get the Git directory (``GIT_DIR``).

    This path is platform-specific. On Windows, the Roaming AppData directory will be used.

    Returns
    -------
    Path
        The path to the Git directory.
    """
    return platformdirs.user_data_path('home-git', roaming=True)


def get_config() -> BaldwinConfigContainer:
    """
    Get the configuration (TOML file).

    Returns
    -------
    BaldwinConfigContainer
        Parsed configuration, or an empty mapping if the file does not exist.
    """
    config_file = platformdirs.user_config_path('baldwin', roaming=True) / 'config.toml'
    if not config_file.exists():
        return {}
    return cast('BaldwinConfigContainer', tomlkit.loads(config_file.read_text()).unwrap())


def get_repo() -> Repo:
    """
    Get a :py:class:`git.Repo` object.

    Also disables GPG signing for the repository.

    Returns
    -------
    Repo
        The repository object.
    """
    repo = Repo(get_git_path(), expand_vars=False)
    repo.git.execute(('git', 'config', 'commit.gpgsign', 'false'))
    return repo


async def _run_prettier(cmd: tuple[str, ...], semaphore: asyncio.Semaphore) -> None:
    """
    Run a single Prettier invocation under a concurrency semaphore.

    Parameters
    ----------
    cmd : tuple[str, ...]
        The full command-line arguments, including the Prettier executable.
    semaphore : asyncio.Semaphore
        Semaphore bounding concurrent Prettier processes.
    """
    async with semaphore:
        log.debug('Running: %s', ' '.join(quote(x) for x in cmd))
        process = await asyncio.create_subprocess_exec(*cmd)
        await process.wait()


async def format_(filenames: Iterable[Path | str] | None = None,
                  log_level: Literal['silent', 'error', 'warn', 'log', 'debug'] = 'error') -> None:
    """
    Format untracked and modified files in the repository.

    Does nothing if Prettier is not in ``PATH``. Each file is formatted by a separate Prettier
    process; invocations run concurrently, bounded by the number of available CPUs.

    The following plugins will be detected and enabled if found:

    * @prettier/plugin-xml
    * prettier-plugin-ini
    * prettier-plugin-sort-json
    * prettier-plugin-toml

    Parameters
    ----------
    filenames : Iterable[Path | str] | None
        Paths to format, or ``None`` to format modified and untracked files under the home
        directory.
    log_level : Literal['silent', 'error', 'warn', 'log', 'debug']
        Value for Prettier's ``--log-level`` option.
    """
    if filenames is None:
        repo = get_repo()
        home = anyio.Path(Path.home())
        untracked = [home / y for y in repo.untracked_files]
        keep = await asyncio.gather(*(_classify_untracked(p) for p in untracked))
        filenames = (*(Path.home() / d.a_path
                       for d in repo.index.diff(None) if d.a_path is not None),
                     *(Path(p) for p in keep if p is not None))
    if not (filenames := list(filenames)):
        log.debug('No files to format.')
        return
    if not (prettier := which('prettier')):
        log.debug('Prettier not found in PATH.')
        return
    with resources.path('baldwin.resources', 'prettier.config.json') as default_config_file:
        config_file = get_config().get('baldwin', {
            'prettier_config': str(default_config_file)
        }).get('prettier_config')
        prettier_real = await anyio.Path(prettier).resolve(strict=True)
        node_modules_path = await (prettier_real.parent / '../..').resolve(strict=True)
        plugin_modules = ('@prettier/plugin-xml/src/plugin.js', 'prettier-plugin-ini/src/plugin.js',
                          'prettier-plugin-sort-json/dist/index.js',
                          'prettier-plugin-toml/lib/index.cjs')
        plugin_paths = [node_modules_path / module for module in plugin_modules]
        plugin_exists = await asyncio.gather(*(p.exists() for p in plugin_paths))
        cmd_prefix = (
            prettier, '--config', str(config_file), '--write', '--no-error-on-unmatched-pattern',
            '--ignore-unknown', '--log-level', log_level,
            *chain(*(('--plugin', str(fp))
                     for fp, exists in zip(plugin_paths, plugin_exists, strict=True) if exists)))
        semaphore = asyncio.Semaphore(_MAX_PARALLEL_PRETTIER)
        await asyncio.gather(*(_run_prettier((*cmd_prefix, str(filename)), semaphore)
                               for filename in filenames))


def set_git_env_vars() -> None:
    """Set environment variables for Git."""
    os.environ['GIT_DIR'] = str(get_git_path())
    os.environ['GIT_WORK_TREE'] = str(Path.home())
