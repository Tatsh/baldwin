from baldwin.main import baldwin_main
from click.testing import CliRunner
from pytest_mock import MockerFixture


def test_format_no_prettier(runner: CliRunner, mocker: MockerFixture) -> None:
    path = mocker.patch('baldwin.lib.Path')
    mocker.patch('baldwin.lib.platformdirs.user_data_path')
    mocker.patch('baldwin.lib.resources')
    run = mocker.patch('baldwin.lib.sp.run')
    which = mocker.patch('baldwin.lib.which')
    which.return_value = None
    repo = mocker.patch('baldwin.lib.Repo')
    repo.untracked_files = ['untracked1']
    changed_file = mocker.MagicMock()
    changed_file.a_path = 'changed1'
    deleted_file = mocker.MagicMock()
    deleted_file.a_path = 'deleted1'
    repo.return_value.index.diff.return_value = [changed_file, deleted_file]
    path.home.return_value.__truediv__.return_value.exists.side_effect = [True, False, True, False]
    runner.invoke(baldwin_main, ('format',))
    assert not run.called


def test_format_no_files(runner: CliRunner, mocker: MockerFixture) -> None:
    mocker.patch('baldwin.lib.Path')
    mocker.patch('baldwin.lib.platformdirs.user_data_path')
    mocker.patch('baldwin.lib.resources')
    run = mocker.patch('baldwin.lib.sp.run')
    which = mocker.patch('baldwin.lib.which')
    repo = mocker.patch('baldwin.lib.Repo')
    repo.untracked_files = []
    repo.return_value.index.diff.return_value = []
    runner.invoke(baldwin_main, ('format',))
    assert not run.called
    assert not which.called


def test_format(runner: CliRunner, mocker: MockerFixture) -> None:
    path = mocker.patch('baldwin.lib.Path')
    mocker.patch('baldwin.lib.platformdirs.user_data_path')
    mocker.patch('baldwin.lib.resources')
    run = mocker.patch('baldwin.lib.sp.run')
    which = mocker.patch('baldwin.lib.which')
    which.return_value = '/bin/prettier'
    repo = mocker.patch('baldwin.lib.Repo')
    repo.untracked_files = ['untracked1']
    changed_file = mocker.MagicMock()
    changed_file.a_path = 'changed1'
    deleted_file = mocker.MagicMock()
    deleted_file.a_path = 'deleted1'
    repo.return_value.index.diff.return_value = [changed_file, deleted_file]
    path.home.return_value.__truediv__.return_value.exists.side_effect = [True, False, True, False]
    runner.invoke(baldwin_main, ('format',))
    assert run.called