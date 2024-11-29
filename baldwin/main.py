from datetime import UTC, datetime
from importlib import resources
from pathlib import Path
from shlex import quote
from shutil import which
import logging
import os
import subprocess as sp

from binaryornot.check import is_binary
from git import Actor, Repo
import click

from .utils import format_, get_git_path, get_repo

log = logging.getLogger(__name__)

__all__ = ('baldwin_main', 'git')


@click.group(context_settings={'help_option_names': ('-h', '--help')})
@click.option('-d', '--debug', help='Enable debug logging.', is_flag=True)
def baldwin_main(*, debug: bool = False) -> None:
    """Manage a home directory with Git."""
    os.environ['GIT_DIR'] = str(get_git_path())
    os.environ['GIT_WORK_TREE'] = str(Path.home())
    logging.basicConfig(level=logging.DEBUG if debug else logging.ERROR)


@click.command(context_settings={
    'help_option_names': ('-h', '--help'),
    'ignore_unknown_options': True
})
@click.argument('args', nargs=-1, type=click.UNPROCESSED)
def git(args: tuple[str, ...]) -> None:
    # Pass these arguments because of the hgit shortcut
    cmd = ('git', f'--git-dir={get_git_path()}', f'--work-tree={Path.home()}', *args)
    log.debug('Running: %s', ' '.join(quote(x) for x in cmd))
    sp.run(cmd, check=False)  # do not use env= because env vars controlling colour will be lost


@click.command(context_settings={'help_option_names': ('-h', '--help')})
def init() -> None:
    """Start tracking a home directory."""
    git_path = get_git_path()
    if not git_path.exists():
        repo = Repo.init(git_path, expand_vars=False)
        repo.git.execute(('git', 'config', 'commit.gpgsign', 'false'))
        gitattributes = Path.home() / '.gitattributes'
        gitattributes.write_text(
            resources.read_text('baldwin.resources', 'default_gitattributes.txt'))
        gitignore = Path.home() / '.gitignore'
        gitignore.write_text(resources.read_text('baldwin.resources', 'default_gitignore.txt'))
        repo.index.add([gitattributes, gitignore])
        if which('jq'):
            repo.git.execute(('git', 'config', 'diff.json.textconv', 'jq -MS .'))
            repo.git.execute(('git', 'config', 'diff.json.cachetextconv', 'true'))
        if (prettier := which('prettier')):
            node_modules_path = (Path(prettier).resolve(strict=True).parent / '..' /
                                 '..').resolve(strict=True)
            if (node_modules_path / '@prettier/plugin-xml/src/plugin.js').exists():
                repo.git.execute(
                    ('git', 'config', 'diff.xml.textconv',
                     'prettier --no-editorconfig --parser xml --xml-whitespace-sensitivity ignore'))
                repo.git.execute(('git', 'config', 'diff.xml.cachetextconv', 'true'))
            repo.git.execute(
                ('git', 'config', 'diff.yaml.textconv', 'prettier --no-editorconfig --parser yaml'))
            repo.git.execute(('git', 'config', 'diff.yaml.cachetextconv', 'true'))


@click.command(context_settings={'help_option_names': ('-h', '--help')})
def auto_commit() -> None:
    """Automatic commit of changed and untracked files."""
    repo = get_repo()
    items_to_add = [
        *[Path.home() / e.a_path for e in repo.index.diff(None)], *[
            x for x in (Path.home() / y
                        for y in repo.untracked_files) if x.is_file() and not is_binary(str(x))
        ]
    ]
    format_(items_to_add)
    repo.index.add(items_to_add)
    repo.index.commit(f'Automatic commit @ {datetime.now(tz=UTC).isoformat()}',
                      committer=Actor('Auto-commiter', 'hgit@tat.sh'))


@click.command(context_settings={'help_option_names': ('-h', '--help')})
def format_main() -> None:
    """Format changed and untracked files."""
    repo = get_repo()
    format_(
        (*(Path.home() / d.a_path for d in repo.index.diff(None)),
         *(x for x in (Path.home() / y
                       for y in repo.untracked_files) if x.is_file() and not is_binary(str(x)))))


@click.command(context_settings={'help_option_names': ('-h', '--help')})
def info() -> None:
    """Get basic information about the repository."""
    click.echo(f'git-dir path: {get_git_path()}')
    click.echo(f'work-tree path: {Path.home()}')


@click.command(context_settings={'help_option_names': ('-h', '--help')})
def install_units() -> None:
    """Install systemd units for automatic committing."""
    bw = which('bw')
    assert bw is not None
    bw_p = Path(bw).resolve(strict=True)
    service_file = Path('~/.config/systemd/user/home-vcs.service').expanduser()
    service_file.write_text(f"""[Unit]
Description=Home directory VCS commit

[Service]
Type=oneshot
ExecStart={bw_p} auto-commit
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


baldwin_main.add_command(auto_commit, 'auto-commit')
baldwin_main.add_command(format_main, 'format')
baldwin_main.add_command(git)
baldwin_main.add_command(info)
baldwin_main.add_command(init)
baldwin_main.add_command(install_units)
