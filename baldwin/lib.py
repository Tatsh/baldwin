"""Baldwin library."""
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import UTC, datetime
from importlib import resources
from itertools import chain
from pathlib import Path
from shlex import quote
from shutil import which
from typing import Literal
import logging
import os
import subprocess as sp

from binaryornot.check import is_binary
from git import Actor, Repo
import platformdirs

log = logging.getLogger(__name__)


def git(args: Iterable[str]) -> None:
    """Front-end to git with git-dir and work-tree passed."""
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


def auto_commit() -> None:
    """Automated commit of changed and untracked files."""
    repo = get_repo()
    diff_items = [Path.home() / e.a_path for e in repo.index.diff(None)]  # pragma: no cover
    items_to_add = [
        *[p for p in diff_items if p.exists()], *[
            x for x in (Path.home() / y
                        for y in repo.untracked_files) if x.is_file() and not is_binary(str(x))
        ]
    ]
    items_to_remove = [p for p in diff_items if not p.exists()]  # pragma: no cover
    if items_to_add:
        format_(items_to_add)
        repo.index.add(items_to_add)
    if items_to_remove:
        repo.index.remove(items_to_remove)
    if items_to_add or items_to_remove:
        repo.index.commit(f'Automatic commit @ {datetime.now(tz=UTC).isoformat()}',
                          committer=Actor('Auto-commiter', 'hgit@tat.sh'))


@dataclass
class RepoInfo:
    """General repository information."""
    git_dir_path: Path
    """Git directory."""
    work_tree_path: Path
    """Work tree."""


def repo_info() -> RepoInfo:
    """Get general repository information."""
    return RepoInfo(git_dir_path=get_git_path(), work_tree_path=Path.home())


def install_units() -> None:
    """Install systemd units for automatic committing."""
    bw = which('bw')
    if not bw:
        raise FileNotFoundError
    service_file = Path('~/.config/systemd/user/home-vcs.service').expanduser()
    service_file.write_text(f"""[Unit]
Description=Home directory VCS commit

[Service]
Type=oneshot
ExecStart={bw} auto-commit
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
    sp.run(('systemctl', '--user', 'daemon-reload'), check=True)


def get_git_path() -> Path:
    """
    Get the Git directory (``GIT_DIR``).

    This path is platform-specific. On Windows, the Roaming AppData directory will be used.
    """
    return platformdirs.user_data_path('home-git', roaming=True)


def get_repo() -> Repo:
    """
    Get a :py:class:`git.Repo` object.

    Also disables GPG signing for the repository.
    """
    repo = Repo(get_git_path(), expand_vars=False)
    repo.git.execute(('git', 'config', 'commit.gpgsign', 'false'))
    return repo


def format_(filenames: Iterable[Path | str] | None = None,
            log_level: Literal['silent', 'error', 'warn', 'log', 'debug'] = 'error') -> None:
    """
    Format untracked and modified files in the repository.

    Does nothing if Prettier is not in ``PATH``.

    The following plugins will be detected and enabled if found:

    * @prettier/plugin-xml
    * prettier-plugin-ini
    * prettier-plugin-sort-json
    * prettier-plugin-toml
    """
    if filenames is None:
        repo = get_repo()
        filenames = (*(Path.home() / d.a_path for d in repo.index.diff(None)),
                     *(x for x in (Path.home() / y for y in repo.untracked_files)
                       if x.is_file() and not is_binary(str(x))))
    if not (filenames := list(filenames)):
        return
    with resources.path('baldwin.resources', 'prettier.config.json') as config_file:
        if not (prettier := which('prettier')):
            return
        # Detect plugins
        node_modules_path = (Path(prettier).resolve(strict=True).parent / '..' /
                             '..').resolve(strict=True)
        cmd_prefix = (prettier, '--config', str(config_file), '--write',
                      '--no-error-on-unmatched-pattern', '--ignore-unknown', '--log-level',
                      log_level, *chain(*(('--plugin', str(fp))
                                          for module in ('@prettier/plugin-xml/src/plugin.js',
                                                         'prettier-plugin-ini/src/plugin.js',
                                                         'prettier-plugin-sort-json/dist/index.js',
                                                         'prettier-plugin-toml/lib/index.cjs')
                                          if (fp := (node_modules_path / module)).exists())))
        for filename in filenames:
            cmd = (*cmd_prefix, str(filename))
            log.debug('Running: %s', ' '.join(quote(x) for x in cmd))
            sp.run(cmd, check=False)


def set_git_env_vars() -> None:
    """Set environment variables for Git."""
    os.environ['GIT_DIR'] = str(get_git_path())
    os.environ['GIT_WORK_TREE'] = str(Path.home())
