from __future__ import annotations

from typing import TYPE_CHECKING

from baldwin.main import baldwin

if TYPE_CHECKING:
    from click.testing import CliRunner
    from pytest_mock import MockerFixture


def _make_fake_process(mocker: MockerFixture) -> object:
    """
    Create a fake :py:class:`asyncio.subprocess.Process` whose ``wait`` is awaitable.

    Parameters
    ----------
    mocker : MockerFixture
        The pytest-mock fixture.

    Returns
    -------
    object
        A mock with an awaitable ``wait`` returning ``0``.
    """
    process = mocker.MagicMock()
    process.wait = mocker.AsyncMock(return_value=0)
    return process


def _mock_anyio_path(mocker: MockerFixture, *, exists: bool = True, is_file: bool = True) -> object:
    """
    Install a mocked ``anyio.Path`` for tests.

    ``__truediv__``, ``parent``, and every async method all return the same configurable
    mock so arbitrary path traversal works.

    Parameters
    ----------
    mocker : MockerFixture
        The pytest-mock fixture.
    exists : bool
        Value returned by every ``exists`` call.
    is_file : bool
        Value returned by every ``is_file`` call.

    Returns
    -------
    object
        The patched ``anyio.Path`` mock.
    """
    anyio_path = mocker.patch('baldwin.lib.anyio.Path')
    node = anyio_path.return_value
    node.__truediv__.return_value = node
    node.parent = node
    node.exists = mocker.AsyncMock(return_value=exists)
    node.is_file = mocker.AsyncMock(return_value=is_file)
    handle = mocker.AsyncMock()
    handle.aclose = mocker.AsyncMock()
    node.open = mocker.AsyncMock(return_value=handle)
    node.resolve = mocker.AsyncMock(return_value=node)
    return anyio_path


def test_format_no_prettier(runner: CliRunner, mocker: MockerFixture) -> None:
    mocker.patch('baldwin.lib.Path')
    mocker.patch('baldwin.lib.platformdirs.user_data_path')
    mocker.patch('baldwin.lib.resources')
    mocker.patch('baldwin.lib.is_binary', return_value=False)
    create = mocker.patch('baldwin.lib.asyncio.create_subprocess_exec',
                          new=mocker.AsyncMock(return_value=_make_fake_process(mocker)))
    which = mocker.patch('baldwin.lib.which')
    which.return_value = None
    repo = mocker.patch('baldwin.lib.Repo')
    repo.return_value.untracked_files = ['untracked1']
    changed_file = mocker.MagicMock()
    changed_file.a_path = 'changed1'
    deleted_file = mocker.MagicMock()
    deleted_file.a_path = 'deleted1'
    repo.return_value.index.diff.return_value = [changed_file, deleted_file]
    _mock_anyio_path(mocker)
    runner.invoke(baldwin, ('format',))
    assert not create.called


def test_format_no_files(runner: CliRunner, mocker: MockerFixture) -> None:
    mocker.patch('baldwin.lib.Path')
    mocker.patch('baldwin.lib.platformdirs.user_data_path')
    mocker.patch('baldwin.lib.resources')
    create = mocker.patch('baldwin.lib.asyncio.create_subprocess_exec',
                          new=mocker.AsyncMock(return_value=_make_fake_process(mocker)))
    which = mocker.patch('baldwin.lib.which')
    repo = mocker.patch('baldwin.lib.Repo')
    repo.return_value.untracked_files = []
    repo.return_value.index.diff.return_value = []
    _mock_anyio_path(mocker)
    runner.invoke(baldwin, ('format',))
    assert not create.called
    assert not which.called


def test_format(runner: CliRunner, mocker: MockerFixture) -> None:
    mocker.patch('baldwin.lib.Path')
    mocker.patch('baldwin.lib.platformdirs.user_data_path')
    mocker.patch('baldwin.lib.platformdirs.user_config_path'
                 ).return_value.__truediv__.return_value.exists.return_value = False
    mocker.patch('baldwin.lib.resources')
    mocker.patch('baldwin.lib.is_binary', return_value=False)
    create = mocker.patch('baldwin.lib.asyncio.create_subprocess_exec',
                          new=mocker.AsyncMock(return_value=_make_fake_process(mocker)))
    which = mocker.patch('baldwin.lib.which')
    which.return_value = '/bin/prettier'
    repo = mocker.patch('baldwin.lib.Repo')
    repo.return_value.untracked_files = ['untracked1']
    changed_file = mocker.MagicMock()
    changed_file.a_path = 'changed1'
    deleted_file = mocker.MagicMock()
    deleted_file.a_path = 'deleted1'
    repo.return_value.index.diff.return_value = [changed_file, deleted_file]
    _mock_anyio_path(mocker)
    runner.invoke(baldwin, ('format',))
    assert create.called


def test_format_config_file_exists(runner: CliRunner, mocker: MockerFixture) -> None:
    mocker.patch('baldwin.lib.Path')
    mocker.patch('baldwin.lib.platformdirs.user_data_path')
    mocker.patch('baldwin.lib.platformdirs.user_config_path'
                 ).return_value.__truediv__.return_value.exists.return_value = True
    mocker.patch('baldwin.lib.resources')
    mocker.patch('baldwin.lib.is_binary', return_value=False)
    mocker.patch('baldwin.lib.tomlkit.loads').return_value.unwrap.return_value = {}
    create = mocker.patch('baldwin.lib.asyncio.create_subprocess_exec',
                          new=mocker.AsyncMock(return_value=_make_fake_process(mocker)))
    which = mocker.patch('baldwin.lib.which')
    which.return_value = '/bin/prettier'
    repo = mocker.patch('baldwin.lib.Repo')
    repo.return_value.untracked_files = ['untracked1']
    changed_file = mocker.MagicMock()
    changed_file.a_path = 'changed1'
    deleted_file = mocker.MagicMock()
    deleted_file.a_path = 'deleted1'
    repo.return_value.index.diff.return_value = [changed_file, deleted_file]
    _mock_anyio_path(mocker)
    runner.invoke(baldwin, ('format',))
    assert create.called
