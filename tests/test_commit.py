from __future__ import annotations

from typing import TYPE_CHECKING

from baldwin.main import baldwin

if TYPE_CHECKING:
    from click.testing import CliRunner
    from pytest_mock import MockerFixture


def _mock_anyio_path(mocker: MockerFixture,
                     *,
                     exists: object,
                     is_file: object = True,
                     open_side_effect: BaseException | type[BaseException] | None = None) -> None:
    """
    Install a mocked ``anyio.Path`` for tests.

    ``__truediv__``, ``parent``, and every async method all return the same configurable
    mock so arbitrary path traversal works.

    Parameters
    ----------
    mocker : MockerFixture
        The pytest-mock fixture.
    exists : object
        Either a single boolean or a list of booleans passed to ``exists.side_effect``.
    is_file : object
        Either a single boolean or a list of booleans passed to ``is_file.side_effect``.
    open_side_effect : BaseException | type[BaseException] | None
        If provided, ``open`` raises this on every call.
    """
    anyio_path = mocker.patch('baldwin.lib.anyio.Path')
    node = anyio_path.return_value
    node.__truediv__.return_value = node
    node.parent = node
    if isinstance(exists, list):
        node.exists = mocker.AsyncMock(side_effect=exists)
    else:
        node.exists = mocker.AsyncMock(return_value=exists)
    if isinstance(is_file, list):
        node.is_file = mocker.AsyncMock(side_effect=is_file)
    else:
        node.is_file = mocker.AsyncMock(return_value=is_file)
    if open_side_effect is not None:
        node.open = mocker.AsyncMock(side_effect=open_side_effect)
    else:
        handle = mocker.AsyncMock()
        handle.aclose = mocker.AsyncMock()
        node.open = mocker.AsyncMock(return_value=handle)
    node.resolve = mocker.AsyncMock(return_value=node)


def test_commit(runner: CliRunner, mocker: MockerFixture) -> None:
    mocker.patch('baldwin.lib.Path')
    mocker.patch('baldwin.lib.platformdirs.user_data_path')
    mocker.patch('baldwin.lib.resources')
    mocker.patch('baldwin.lib.is_binary', return_value=False)
    which = mocker.patch('baldwin.lib.which')
    which.return_value = None
    repo = mocker.patch('baldwin.lib.Repo')
    repo.return_value.untracked_files = ['untracked1']
    changed_file = mocker.MagicMock()
    changed_file.a_path = 'changed1'
    deleted_file = mocker.MagicMock()
    deleted_file.a_path = 'deleted1'
    repo.return_value.index.diff.return_value = [changed_file, deleted_file]
    _mock_anyio_path(mocker, exists=[True, False])
    runner.invoke(baldwin, ('auto-commit',))
    assert repo.return_value.index.add.called
    assert repo.return_value.index.remove.called
    assert repo.return_value.index.commit.called


def test_commit_no_files(runner: CliRunner, mocker: MockerFixture) -> None:
    mocker.patch('baldwin.lib.Path')
    mocker.patch('baldwin.lib.platformdirs.user_data_path')
    mocker.patch('baldwin.lib.resources')
    which = mocker.patch('baldwin.lib.which')
    which.return_value = None
    repo = mocker.patch('baldwin.lib.Repo')
    repo.return_value.untracked_files = []
    repo.return_value.index.diff.return_value = []
    _mock_anyio_path(mocker, exists=True)
    runner.invoke(baldwin, ('auto-commit',))
    assert not repo.return_value.index.add.called
    assert not repo.return_value.index.remove.called
    assert not repo.return_value.index.commit.called


def test_commit_no_add(runner: CliRunner, mocker: MockerFixture) -> None:
    mocker.patch('baldwin.lib.Path')
    mocker.patch('baldwin.lib.platformdirs.user_data_path')
    mocker.patch('baldwin.lib.resources')
    which = mocker.patch('baldwin.lib.which')
    which.return_value = None
    repo = mocker.patch('baldwin.lib.Repo')
    repo.return_value.untracked_files = []
    deleted_file = mocker.MagicMock()
    deleted_file.a_path = 'deleted1'
    repo.return_value.index.diff.return_value = [deleted_file]
    _mock_anyio_path(mocker, exists=False)
    runner.invoke(baldwin, ('auto-commit',))
    assert not repo.return_value.index.add.called
    assert repo.return_value.index.remove.called
    assert repo.return_value.index.commit.called


def test_commit_no_delete(runner: CliRunner, mocker: MockerFixture) -> None:
    mocker.patch('baldwin.lib.Path')
    mocker.patch('baldwin.lib.platformdirs.user_data_path')
    mocker.patch('baldwin.lib.resources')
    mocker.patch('baldwin.lib.is_binary', return_value=False)
    which = mocker.patch('baldwin.lib.which')
    which.return_value = None
    repo = mocker.patch('baldwin.lib.Repo')
    repo.return_value.untracked_files = ['untracked1']
    changed_file = mocker.MagicMock()
    changed_file.a_path = 'changed1'
    repo.return_value.index.diff.return_value = [changed_file]
    _mock_anyio_path(mocker, exists=True)
    runner.invoke(baldwin, ('auto-commit',))
    assert repo.return_value.index.add.called
    assert not repo.return_value.index.remove.called
    assert repo.return_value.index.commit.called


def test_commit_ignore_unreadable_files(runner: CliRunner, mocker: MockerFixture) -> None:
    mocker.patch('baldwin.lib.Path')
    mocker.patch('baldwin.lib.platformdirs.user_data_path')
    mocker.patch('baldwin.lib.resources')
    which = mocker.patch('baldwin.lib.which')
    which.return_value = None
    repo = mocker.patch('baldwin.lib.Repo')
    repo.return_value.untracked_files = ['untracked1']
    changed_file = mocker.MagicMock()
    changed_file.a_path = 'changed1'
    deleted_file = mocker.MagicMock()
    deleted_file.a_path = 'deleted1'
    repo.return_value.index.diff.return_value = [changed_file, deleted_file]
    _mock_anyio_path(mocker, exists=[True, False], is_file=True, open_side_effect=PermissionError)
    runner.invoke(baldwin, ('auto-commit',))
    assert len(repo.return_value.index.add.call_args[0][0]) == 1
    assert repo.return_value.index.remove.called
    assert repo.return_value.index.commit.called


def test_commit_ignore_binary_untracked_files(runner: CliRunner, mocker: MockerFixture) -> None:
    mocker.patch('baldwin.lib.Path')
    mocker.patch('baldwin.lib.platformdirs.user_data_path')
    mocker.patch('baldwin.lib.resources')
    mocker.patch('baldwin.lib.is_binary', return_value=True)
    which = mocker.patch('baldwin.lib.which')
    which.return_value = None
    repo = mocker.patch('baldwin.lib.Repo')
    repo.return_value.untracked_files = ['untracked1']
    changed_file = mocker.MagicMock()
    changed_file.a_path = 'changed1'
    repo.return_value.index.diff.return_value = [changed_file]
    _mock_anyio_path(mocker, exists=True, is_file=True)
    runner.invoke(baldwin, ('auto-commit',))
    assert len(repo.return_value.index.add.call_args[0][0]) == 1
    assert not repo.return_value.index.remove.called
    assert repo.return_value.index.commit.called
