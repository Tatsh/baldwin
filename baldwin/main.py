"""Commands."""
from __future__ import annotations

import logging

import click

from .lib import (
    auto_commit as auto_commit_,
    format_,
    git as git_,
    init as init_,
    install_units as install_units_,
    repo_info,
    set_git_env_vars,
)
from .utils import setup_logging

log = logging.getLogger(__name__)

__all__ = ('baldwin', 'git')


@click.group(context_settings={'help_option_names': ('-h', '--help')})
@click.option('-d', '--debug', help='Enable debug logging.', is_flag=True)
def baldwin(*, debug: bool = False) -> None:
    """Manage a home directory with Git."""
    set_git_env_vars()
    setup_logging(debug=debug)


@click.command(context_settings={
    'help_option_names': ('-h', '--help'),
    'ignore_unknown_options': True
})
@click.argument('args', nargs=-1, type=click.UNPROCESSED)
def git(args: tuple[str, ...]) -> None:
    """Wrap git with git-dir and work-tree passed."""
    git_(args)


@click.command(context_settings={'help_option_names': ('-h', '--help')})
def init() -> None:
    """Start tracking a home directory."""
    init_()


@click.command(context_settings={'help_option_names': ('-h', '--help')})
def auto_commit() -> None:
    """Automated commit of changed and untracked files."""
    auto_commit_()


@click.command(context_settings={'help_option_names': ('-h', '--help')})
def format() -> None:  # noqa: A001
    """Format changed and untracked files."""
    format_()


@click.command(context_settings={'help_option_names': ('-h', '--help')})
def info() -> None:
    """Get basic information about the repository."""
    data = repo_info()
    click.echo(f'git-dir path: {data.git_dir_path}')
    click.echo(f'work-tree path: {data.work_tree_path}')


@click.command(context_settings={'help_option_names': ('-h', '--help')})
def install_units() -> None:
    """Install systemd units for automatic committing."""
    install_units_()


baldwin.add_command(auto_commit)
baldwin.add_command(format)
baldwin.add_command(git)
baldwin.add_command(info)
baldwin.add_command(init)
baldwin.add_command(install_units)
