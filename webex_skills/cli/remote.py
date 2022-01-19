import json
from pathlib import Path
from pprint import pformat
from typing import Optional

import typer

from .config import get_remotes

remote = typer.Typer(name='remote', help='Commands for interacting with running skills')


def prompt_for_secret():
    secret: str = typer.prompt('Secret', hide_input=True)
    while not len(secret) > 20:
        typer.echo('Secrets must be at least 20 characters')
        secret = typer.prompt('Secret', hide_input=True)
    return secret


def prompt_for_key():
    public_key_path = Path(typer.prompt('Public key path', Path('./id_rsa.pub')))
    if public_key_path.exists():
        return public_key_path

    while True:
        typer.secho(f'The path {public_key_path} does not exist, please try again', color=typer.colors.RED)
        public_key_path = Path(typer.prompt('Public key path', public_key_path))
        if public_key_path.exists():
            return public_key_path


@remote.command()
def create(
    name: str = typer.Argument(..., help="The name to give to the remote."),
    url: Optional[str] = typer.Option(None, '-u', help="URL of the remote. If not provided it will be requested."),
    secret: Optional[str] = typer.Option(
        None, '--secret', '-s', help="The skill secret. If not provided it will be requested."
    ),
    public_key_path: Optional[Path] = typer.Option(
        None, '-k', '--key', help="The path to the public key. If not provided it will be requested."
    ),
):
    """Add configuration for a new remote skill to the cli config file"""
    app_dir = Path(typer.get_app_dir('skills-cli', force_posix=True))
    config_file = app_dir / 'config.json'

    if not app_dir.exists():
        app_dir.mkdir(parents=True)

    if config_file.exists():
        config = json.loads(config_file.read_text(encoding='utf-8'))
    else:
        typer.secho(f'Config file {config_file} not found, creating...')
        config_file.touch()
        config = {}

    remotes = config.get('remotes', {})
    existing_config = remotes.get(name, {})
    if existing_config:
        typer.confirm(
            f'A configuration with the name "{name}" already exists, would you like to overwrite it?', abort=True
        )

    if not secret:
        secret = prompt_for_secret()

    if not public_key_path:
        public_key_path = prompt_for_key()

    if not url:
        url = typer.prompt('URL to invoke the skill', default='http://localhost:8080/parse')

    remotes[name] = {'name': name, 'url': url, 'secret': secret, 'public_key_path': str(public_key_path.absolute())}
    config['remotes'] = remotes
    config_file.write_text(json.dumps(config, indent=2), encoding='utf-8')


@remote.command('list')
def ls(
    name: Optional[str] = typer.Option(None, help="The name of a particular skill to display.")
):  # pylint:disable=invalid-name
    """List configured remote skills"""
    remotes = get_remotes()
    if not remotes:
        typer.secho('No configured remotes found', color=typer.colors.RED, err=True)
        raise typer.Exit(1)

    if name:
        remote_config = remotes.get(name)
        if not remote_config:
            typer.secho(f'No configured remote with the name {name} found', color=typer.colors.RED, err=True)
            raise typer.Exit(1)
    else:
        remote_config = remotes

    typer.echo(pformat(remote_config))
