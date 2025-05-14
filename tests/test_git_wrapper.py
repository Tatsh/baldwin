from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from baldwin.lib import get_git_path
from baldwin.main import baldwin, git

if TYPE_CHECKING:
    from click.testing import CliRunner
    from pytest_mock import MockerFixture


def test_hgit_wrapper(runner: CliRunner, mocker: MockerFixture) -> None:
    run = mocker.patch('baldwin.lib.sp.run')
    runner.invoke(git, ('status',))
    run.assert_called_once_with(
        ('git', f'--git-dir={get_git_path()}', f'--work-tree={Path.home()}', 'status'), check=False)


def test_bw_git_wrapper(runner: CliRunner, mocker: MockerFixture) -> None:
    run = mocker.patch('baldwin.lib.sp.run')
    runner.invoke(baldwin, ('git', 'status'))
    run.assert_called_once_with(
        ('git', f'--git-dir={get_git_path()}', f'--work-tree={Path.home()}', 'status'), check=False)
