from baldwin.main import baldwin_main
from click.testing import CliRunner
from pytest_mock import MockerFixture


def test_commit(runner: CliRunner, mocker: MockerFixture) -> None:
    path = mocker.patch('baldwin.lib.Path')
    mocker.patch('baldwin.lib.platformdirs.user_data_path')
    mocker.patch('baldwin.lib.resources')
    which = mocker.patch('baldwin.lib.which')
    which.return_value = None  # Disable format
    repo = mocker.patch('baldwin.lib.Repo')
    repo.untracked_files = ['untracked1']
    changed_file = mocker.MagicMock()
    changed_file.a_path = 'changed1'
    deleted_file = mocker.MagicMock()
    deleted_file.a_path = 'deleted1'
    repo.return_value.index.diff.return_value = [changed_file, deleted_file]
    path.home.return_value.__truediv__.return_value.exists.side_effect = [True, False, True, False]
    runner.invoke(baldwin_main, ('auto-commit',))
    assert repo.return_value.index.add.called
    assert repo.return_value.index.remove.called
    assert repo.return_value.index.commit.called


def test_commit_no_files(runner: CliRunner, mocker: MockerFixture) -> None:
    mocker.patch('baldwin.lib.Path')
    mocker.patch('baldwin.lib.platformdirs.user_data_path')
    mocker.patch('baldwin.lib.resources')
    which = mocker.patch('baldwin.lib.which')
    which.return_value = None  # Disable format
    repo = mocker.patch('baldwin.lib.Repo')
    repo.untracked_files = []
    repo.return_value.index.diff.return_value = []
    runner.invoke(baldwin_main, ('auto-commit',))
    assert not repo.return_value.index.add.called
    assert not repo.return_value.index.remove.called
    assert not repo.return_value.index.commit.called


def test_commit_no_add(runner: CliRunner, mocker: MockerFixture) -> None:
    path = mocker.patch('baldwin.lib.Path')
    mocker.patch('baldwin.lib.platformdirs.user_data_path')
    mocker.patch('baldwin.lib.resources')
    which = mocker.patch('baldwin.lib.which')
    which.return_value = None  # Disable format
    repo = mocker.patch('baldwin.lib.Repo')
    repo.untracked_files = []
    deleted_file = mocker.MagicMock()
    deleted_file.a_path = 'deleted1'
    repo.return_value.index.diff.return_value = [deleted_file]
    path.home.return_value.__truediv__.return_value.exists.return_value = False
    runner.invoke(baldwin_main, ('auto-commit',))
    assert not repo.return_value.index.add.called
    assert repo.return_value.index.remove.called
    assert repo.return_value.index.commit.called


def test_commit_no_delete(runner: CliRunner, mocker: MockerFixture) -> None:
    mocker.patch('baldwin.lib.Path')
    mocker.patch('baldwin.lib.platformdirs.user_data_path')
    mocker.patch('baldwin.lib.resources')
    which = mocker.patch('baldwin.lib.which')
    which.return_value = None  # Disable format
    repo = mocker.patch('baldwin.lib.Repo')
    repo.untracked_files = ['untracked1']
    changed_file = mocker.MagicMock()
    changed_file.a_path = 'changed1'
    repo.return_value.index.diff.return_value = [changed_file]
    runner.invoke(baldwin_main, ('auto-commit',))
    assert repo.return_value.index.add.called
    assert not repo.return_value.index.remove.called
    assert repo.return_value.index.commit.called