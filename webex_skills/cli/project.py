import json
from pathlib import Path
import secrets
import shutil
from typing import Optional

import typer

from ..crypto import generate_keys
from .config import CONFIG_DIR, CONFIG_FILE, get_remotes, get_skill_config
from .helpers import create_nlp

app = typer.Typer(name='project')


@app.command(name='init')
def init(
    skill_name: str = typer.Argument(..., help="The name of the skill you want to create"),
    skill_path: Path = typer.Option(
        '.',
        help='Directory in which to initialize a skill project',
        dir_okay=True,
        file_okay=False,
        writable=True,
        resolve_path=True,
    ),
    secret: Optional[str] = typer.Option(
        None, help="A secret for encryption. If not provided, one will be generated automatically."
    ),
    mindmeld: Optional[bool] = typer.Option(
        False,
        help="If flag set, a MindMeld app will be created, otherwise it defaults to a simple app",
        is_flag=True,
    ),
):
    """Create a new skill project from a template"""

    if not CONFIG_DIR.exists():
        CONFIG_DIR.mkdir(parents=True)
    # Check for an existing skill name and provide an option to overwrite
    if CONFIG_FILE.exists() and get_skill_config(skill_name):
        if not typer.confirm(
            f'A skill named {skill_name} already exists in your configuration. Would you like to overwrite it?'
        ):
            return

    if not secret:
        typer.secho('Generating secret...')
        secret = secrets.token_urlsafe(16)

    # TODO: Pass static path down  # pylint:disable=fixme
    typer.secho(f'Generating skill {skill_name} project at {skill_path/skill_name}...')
    if mindmeld:
        create_mm_project(skill_name, skill_path, secret)
        return
    create_simple_project(skill_name, skill_path, secret)


def create_simple_project(skill_name: str, output_dir: Path, secret: str) -> None:
    _create_project(skill_name, output_dir, 'default_app.py', secret)


def create_mm_project(skill_name, output_dir, secret) -> None:
    """Create a mindmeld based project"""
    app_dir = _create_project(skill_name, output_dir, 'mm_app.py', secret=secret)

    # Create MM NLP directory structure
    domains_dir = app_dir / 'domains'
    entities_dir = app_dir / 'entities'
    entities_dir.mkdir()

    static_path = Path(__file__).parent.parent / 'static'
    # Copy sample domains into domain folder
    shutil.copytree(static_path / 'default_domains', domains_dir)

    # Copy app config to avoid requirements
    mm_config_path = static_path / 'mm_config.py'
    shutil.copy(mm_config_path, app_dir / 'config.py')

    # Build models
    typer.secho('Initializing natural language processor', fg=typer.colors.GREEN)
    nlp = create_nlp(str(app_dir))
    typer.secho('Building NLP models', fg=typer.colors.GREEN)
    nlp.build()

    typer.secho('Success!')


def _create_project(
    skill_name: str, output_dir: Path, app_file_name: str, secret: str
):  # pylint:disable=too-many-locals
    output_dir = output_dir / skill_name
    typer.echo(f'Creating project directory {output_dir}')
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate keys
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
    test_path = package_path / 'tests'
    test_path.mkdir()

    static_path = Path(__file__).parent.parent / 'static'

    # Create pyproject.toml
    toml_template = static_path / 'pyproject.toml.tmpl'
    toml_content = toml_template.read_text().format(skill_name=skill_name)
    toml_out_path = output_dir / 'pyproject.toml'
    toml_out_path.write_text(toml_content)

    # Copy appropriate app file
    app_file_path = static_path / app_file_name
    app_file_dest = package_path / 'main.py'
    shutil.copy(app_file_path, app_file_dest)

    app_dir = package_path.absolute()
    # Create env file with default values

    env_template = static_path / 'env.tmpl'
    env_content = env_template.read_text()
    env_content = env_content.format(
        skill_name=skill_name, skill_secret=secret, app_dir=app_dir, private_key_path=priv_path
    )

    env_file_path = output_dir / '.env'
    env_file_path.write_text(env_content)

    remotes = get_remotes()
    remotes[skill_name] = {
        'name': skill_name,
        'url': "http://localhost:8080/parse",
        'secret': secret,
        'public_key_path': str(pub_path.absolute()),
        'private_key_path': str(priv_path.absolute()),
        'project_path': str(output_dir),
        'app_dir': str(app_dir),
    }

    CONFIG_FILE.write_text(json.dumps({'remotes': remotes}, indent=2), encoding='utf-8')
    return app_dir
