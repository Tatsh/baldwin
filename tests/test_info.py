from __future__ import annotations

from typing import TYPE_CHECKING
import re

from baldwin.main import baldwin

if TYPE_CHECKING:
    from click.testing import CliRunner
    from pytest_mock import MockerFixture


def test_init_returns_if_exists(runner: CliRunner, mocker: MockerFixture) -> None:
    mocker.patch('baldwin.lib.platformdirs.user_data_path').return_value.exists.return_value = True
    mocker.patch('baldwin.lib.Path')
    run = runner.invoke(baldwin, ('info',))
    lines = run.stdout.splitlines()
    assert re.match(r'^git-dir path: <MagicMock.*>$', lines[0])
    assert re.match(r'^work-tree path: <MagicMock.*>$', lines[1])
