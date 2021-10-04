import json
from pathlib import Path
import secrets
import shutil
from typing import Optional

import typer

from webex_assistant_sdk.cli.config import get_skill_config
from webex_assistant_sdk.crypto import generate_keys

app = typer.Typer(name='project')

# TODO: Add password support for private key


@app.command(name='init')
def init(
    skill_name: str,
    skill_path: Path = typer.Option(
        '.',
        help='Directory in which to initialize a skill project',
        dir_okay=True,
        file_okay=False,
        writable=True,
        resolve_path=True,
    ),
    secret: Optional[str] = None,
    mindmeld: Optional[bool] = typer.Option(False, is_flag=True),
):
    """Create a new skill project from a template"""
    # TODO: Support private key password

    if not secret:
        typer.secho('Generating secret...')
        secret = secrets.token_urlsafe(16)

    if mindmeld:
        create_mm_project(skill_name, skill_path, secret)
    create_project(skill_name, skill_path, secret)


def create_project(
    skill_name: str,
    output_dir: Path,
    secret: Optional[str] = None,
) -> None:
    typer.secho(
        f'Generating skill {skill_name} project at {output_dir}...',
    )

    # if output_dir.exists() and any(output_dir.iterdir()):
    #     typer.echo(f'The provided path {output_dir} already exists, and is not empty', err=True)
    #     raise typer.Exit(1)

    typer.echo(f'Creating project directory {output_dir}')
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate keys
    # TODO: Factor out key generation cli bits as it's going to be used in multiple places
    typer.secho('🔐 Generating new RSA keypair...', fg=typer.colors.GREEN)
    priv_path = output_dir / 'id_rsa.pem'
    pub_path = output_dir / 'id_rsa.pub'
    generate_keys(priv_path, pub_path)

    # Create directory structure
    package_path = output_dir / skill_name.replace('-', '_')
    package_path.mkdir()

    # Add __init__.py
    init_path = package_path / '__init__.py'
    init_path.touch()

    # Add tests directory
    test_path = output_dir / 'tests'
    test_path.mkdir()

    static_path = Path(__file__).parent.parent / 'static'

    # Create pyproject.toml
    toml_template = static_path / 'pyproject.toml.tmpl'
    toml_content = toml_template.read_text()

    toml_content = toml_content.replace('{{skill_name}}', skill_name)
    toml_out_path = output_dir / 'pyproject.toml'
    toml_out_path.write_text(toml_content)

    # Copy appropriate app file
    app_file_path = static_path / 'default_app.py'
    app_file_dest = package_path / 'app.py'
    shutil.copy(app_file_path, app_file_dest)

    # Create env file with default values
    content = f"SKILLS_SKILL_NAME={skill_name}\n" f"SKILLS_SECRET={secret}\n" f"SKILLS_USE_ENCRYPTION=1\n"

    env_file_path = output_dir / '.env'
    env_file_path.write_text(content)

    config = get_skill_config()
    remotes = config.get('remotes', {})

    remotes[skill_name] = {
        'name': skill_name,
        'url': "http://localhost:8080/parse",
        'secret': secret,
        'public_key_path': str(pub_path.absolute()),
        'project_path': str(package_path.absolute()),
    }
    config['remotes'] = remotes

    app_dir = Path(typer.get_app_dir('skills-cli', force_posix=True))
    config_file = app_dir / 'config.json'

    config_file.write_text(json.dumps(config, indent=2))


def create_mm_project(skill_name, output_dir, secret) -> None:
    """Create a mindmeld based project"""
    pass
