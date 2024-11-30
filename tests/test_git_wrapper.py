from pathlib import Path

from baldwin.lib import get_git_path
from baldwin.main import baldwin_main, git_main
from click.testing import CliRunner
from pytest_mock import MockerFixture


def test_hgit_wrapper(runner: CliRunner, mocker: MockerFixture) -> None:
    run = mocker.patch('baldwin.lib.sp.run')
    runner.invoke(git_main, ('status',))
    run.assert_called_once_with(
        ('git', f'--git-dir={get_git_path()}', f'--work-tree={Path.home()}', 'status'), check=False)


def test_bw_git_wrapper(runner: CliRunner, mocker: MockerFixture) -> None:
    run = mocker.patch('baldwin.lib.sp.run')
    runner.invoke(baldwin_main, ('git', 'status'))
    run.assert_called_once_with(
        ('git', f'--git-dir={get_git_path()}', f'--work-tree={Path.home()}', 'status'), check=False)
