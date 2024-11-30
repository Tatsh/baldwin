import logging

import click

from .lib import (
    auto_commit,
    format_,
    git,
    init,
    install_units,
    repo_info,
    set_git_env_vars,
)

log = logging.getLogger(__name__)

__all__ = ('baldwin_main', 'git_main')


@click.group(context_settings={'help_option_names': ('-h', '--help')})
@click.option('-d', '--debug', help='Enable debug logging.', is_flag=True)
def baldwin_main(*, debug: bool = False) -> None:
    """Manage a home directory with Git."""
    set_git_env_vars()
    logging.basicConfig(level=logging.DEBUG if debug else logging.ERROR)


@click.command(context_settings={
    'help_option_names': ('-h', '--help'),
    'ignore_unknown_options': True
})
@click.argument('args', nargs=-1, type=click.UNPROCESSED)
def git_main(args: tuple[str, ...]) -> None:
    """Wrap git with git-dir and work-tree passed."""
    git(args)


@click.command(context_settings={'help_option_names': ('-h', '--help')})
def init_main() -> None:
    """Start tracking a home directory."""
    init()


@click.command(context_settings={'help_option_names': ('-h', '--help')})
def auto_commit_main() -> None:
    """Automated commit of changed and untracked files."""
    auto_commit()


@click.command(context_settings={'help_option_names': ('-h', '--help')})
def format_main() -> None:
    """Format changed and untracked files."""
    format_()


@click.command(context_settings={'help_option_names': ('-h', '--help')})
def info_main() -> None:
    """Get basic information about the repository."""
    data = repo_info()
    click.echo(f'git-dir path: {data.git_dir_path}')
    click.echo(f'work-tree path: {data.work_tree_path}')


@click.command(context_settings={'help_option_names': ('-h', '--help')})
def install_units_main() -> None:
    """Install systemd units for automatic committing."""
    install_units()


baldwin_main.add_command(auto_commit_main, 'auto-commit')
baldwin_main.add_command(format_main, 'format')
baldwin_main.add_command(git_main, 'git')
baldwin_main.add_command(info_main, 'info')
baldwin_main.add_command(init_main, 'init')
baldwin_main.add_command(install_units_main, 'install-units')
