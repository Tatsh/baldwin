from __future__ import annotations

from typing import TYPE_CHECKING

from baldwin.main import baldwin

if TYPE_CHECKING:
    from click.testing import CliRunner
    from pytest_mock import MockerFixture


def test_install_units_no_bw(runner: CliRunner, mocker: MockerFixture) -> None:
    mocker.patch('baldwin.lib.which').return_value = None
    run = runner.invoke(baldwin, ('install-units',))
    assert run.exit_code != 0


def test_install_units(runner: CliRunner, mocker: MockerFixture) -> None:
    path = mocker.patch('baldwin.lib.Path')
    mocker.patch('baldwin.lib.sp.run')
    runner.invoke(baldwin, ('install-units',))
    service_content = path.return_value.expanduser.return_value.write_text.mock_calls[0].args[0]
    assert 'Type=oneshot' in service_content
    assert 'ExecStart=' in service_content
    timer_content = path.return_value.expanduser.return_value.write_text.mock_calls[1].args[0]
    assert 'OnCalendar=' in timer_content
    assert 'WantedBy=timers.target' in timer_content
