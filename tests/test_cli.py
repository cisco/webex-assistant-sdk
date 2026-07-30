from unittest.mock import patch
from typer.testing import CliRunner
from webex_skills.cli.skill import app

runner = CliRunner()


def test_cli_run_custom_host_and_port():
    fake_config = {
        'project_path': '/tmp/fake',
        'private_key_path': '/tmp/fake.key',
        'secret': 'secret',
        'app_dir': '/tmp/app',
    }

    with (
        patch('webex_skills.cli.skill.get_skill_config', return_value=fake_config),
        patch('webex_skills.cli.skill.uvicorn.run') as mock_uvicorn,
    ):
        result = runner.invoke(app, ['run', 'my_skill', '--host', '0.0.0.0', '--port', '9090'])
        assert result.exit_code == 0
        mock_uvicorn.assert_called_once_with('my_skill.main:api', host='0.0.0.0', port=9090, log_level='info')
