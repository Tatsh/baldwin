"""Commands."""
from __future__ import annotations

import asyncio
import logging

from bascom import setup_logging
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

__all__ = ('baldwin', 'git')

log = logging.getLogger(__name__)


def _setup(*, debug: bool) -> None:
    """
    Prepare the Git environment variables and configure logging for a command.

    Parameters
    ----------
    debug : bool
        Whether to enable debug-level logging.
    """
    set_git_env_vars()
    setup_logging(debug=debug, loggers={'baldwin': {}})


@click.group(context_settings={'help_option_names': ('-h', '--help')})
def baldwin() -> None:
    """Manage a home directory with Git."""


@click.command(context_settings={
    'help_option_names': ('-h', '--help'),
    'ignore_unknown_options': True
})
@click.option('-d', '--debug', help='Enable debug logging.', is_flag=True)
@click.argument('args', nargs=-1, type=click.UNPROCESSED)
def git(args: tuple[str, ...], *, debug: bool = False) -> None:
    """Wrap git with git-dir and work-tree passed."""
    _setup(debug=debug)
    git_(args)


@click.command(context_settings={'help_option_names': ('-h', '--help')})
@click.option('-d', '--debug', help='Enable debug logging.', is_flag=True)
def init(*, debug: bool = False) -> None:
    """Start tracking a home directory."""
    _setup(debug=debug)
    init_()


@click.command(context_settings={'help_option_names': ('-h', '--help')})
@click.option('-d', '--debug', help='Enable debug logging.', is_flag=True)
def auto_commit(*, debug: bool = False) -> None:
    """Automated commit of changed and untracked files."""
    _setup(debug=debug)
    asyncio.run(auto_commit_())


@click.command(context_settings={'help_option_names': ('-h', '--help')})
@click.option('-d', '--debug', help='Enable debug logging.', is_flag=True)
def format(*, debug: bool = False) -> None:  # noqa: A001
    """Format changed and untracked files."""
    _setup(debug=debug)
    asyncio.run(format_())


@click.command(context_settings={'help_option_names': ('-h', '--help')})
@click.option('-d', '--debug', help='Enable debug logging.', is_flag=True)
def info(*, debug: bool = False) -> None:
    """Get basic information about the repository."""
    _setup(debug=debug)
    data = repo_info()
    click.echo(f'git-dir path: {data.git_dir_path}')
    click.echo(f'work-tree path: {data.work_tree_path}')


@click.command(context_settings={'help_option_names': ('-h', '--help')})
@click.option('-d', '--debug', help='Enable debug logging.', is_flag=True)
def install_units(*, debug: bool = False) -> None:
    """Install systemd units for automatic committing."""
    _setup(debug=debug)
    install_units_()


baldwin.add_command(auto_commit)
baldwin.add_command(format)
baldwin.add_command(git)
baldwin.add_command(info)
baldwin.add_command(init)
baldwin.add_command(install_units)
