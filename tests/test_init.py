from __future__ import annotations

from typing import TYPE_CHECKING

from baldwin.main import baldwin

if TYPE_CHECKING:
    from click.testing import CliRunner
    from pytest_mock import MockerFixture


def test_init_returns_if_exists(runner: CliRunner, mocker: MockerFixture) -> None:
    mocker.patch('baldwin.lib.platformdirs.user_data_path').return_value.exists.return_value = True
    repo = mocker.patch('baldwin.lib.Repo')
    runner.invoke(baldwin, ('init',))
    assert not repo.called


def test_init(runner: CliRunner, mocker: MockerFixture) -> None:
    path = mocker.patch('baldwin.lib.Path')
    mocker.patch('baldwin.lib.platformdirs.user_data_path').return_value.exists.return_value = False
    repo = mocker.patch('baldwin.lib.Repo')
    mocker.patch('baldwin.lib.resources')
    which = mocker.patch('baldwin.lib.which')
    which.side_effect = ['jq', 'prettier']
    runner.invoke(baldwin, ('init',))
    assert repo.init.called
    assert repo.init.return_value.index.add.called
    path.home.return_value.__truediv__.assert_any_call('.gitattributes')
    path.home.return_value.__truediv__.assert_any_call('.gitignore')
    assert path.home.return_value.__truediv__.return_value.write_text.call_count == 2
    which.assert_any_call('jq')
    which.assert_any_call('prettier')
    repo.init.return_value.git.execute.assert_any_call(('git', 'config', 'commit.gpgsign', 'false'))
    repo.init.return_value.git.execute.assert_any_call(
        ('git', 'config', 'diff.json.textconv', '"jq" -MS .'))
    repo.init.return_value.git.execute.assert_any_call(
        ('git', 'config', 'diff.xml.textconv',
         '"prettier" --no-editorconfig --parser xml --xml-whitespace-sensitivity ignore'))
    repo.init.return_value.git.execute.assert_any_call(
        ('git', 'config', 'diff.yaml.textconv', '"prettier" --no-editorconfig --parser yaml'))


def test_init_no_tools(runner: CliRunner, mocker: MockerFixture) -> None:
    path = mocker.patch('baldwin.lib.Path')
    mocker.patch('baldwin.lib.platformdirs.user_data_path').return_value.exists.return_value = False
    repo = mocker.patch('baldwin.lib.Repo')
    mocker.patch('baldwin.lib.resources')
    which = mocker.patch('baldwin.lib.which')
    which.return_value = False
    runner.invoke(baldwin, ('init',))
    assert repo.init.called
    path.home.return_value.__truediv__.assert_any_call('.gitattributes')
    path.home.return_value.__truediv__.assert_any_call('.gitignore')
    assert path.home.return_value.__truediv__.return_value.write_text.call_count == 2
    which.assert_any_call('jq')
    which.assert_any_call('prettier')
    repo.init.return_value.git.execute.assert_any_call(('git', 'config', 'commit.gpgsign', 'false'))


def test_init_no_xml_plugin(runner: CliRunner, mocker: MockerFixture) -> None:
    path = mocker.patch('baldwin.lib.Path')
    mocker.patch('baldwin.lib.platformdirs.user_data_path').return_value.exists.return_value = False
    repo = mocker.patch('baldwin.lib.Repo')
    mocker.patch('baldwin.lib.resources')
    which = mocker.patch('baldwin.lib.which')
    which.side_effect = ['jq', 'prettier']
    path.return_value.resolve.return_value.parent.__truediv__.return_value.__truediv__.return_value.resolve.return_value.__truediv__.return_value.exists.return_value = False  # noqa: E501
    runner.invoke(baldwin, ('init',))
    assert repo.init.called
    assert repo.init.return_value.index.add.called
    path.home.return_value.__truediv__.assert_any_call('.gitattributes')
    path.home.return_value.__truediv__.assert_any_call('.gitignore')
    assert path.home.return_value.__truediv__.return_value.write_text.call_count == 2
    which.assert_any_call('jq')
    which.assert_any_call('prettier')
    repo.init.return_value.git.execute.assert_any_call(('git', 'config', 'commit.gpgsign', 'false'))
    repo.init.return_value.git.execute.assert_any_call(
        ('git', 'config', 'diff.json.textconv', '"jq" -MS .'))
    repo.init.return_value.git.execute.assert_any_call(
        ('git', 'config', 'diff.yaml.textconv', '"prettier" --no-editorconfig --parser yaml'))
