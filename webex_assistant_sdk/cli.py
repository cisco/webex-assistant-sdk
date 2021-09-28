import json
import os
from pathlib import Path
from pprint import pprint
import re
import secrets
from typing import Optional

from cookiecutter.main import cookiecutter
from cryptography.hazmat.primitives import serialization
import requests
import typer

from webex_assistant_sdk import crypto

app = typer.Typer()


@app.command()
def invoke(
    secret: Optional[str] = typer.Option(None, '--secret', '-s'),
    public_key_path: Optional[Path] = typer.Option(None, '-k', '--key'),
    url: Optional[str] = typer.Option('http://localhost:8080', '-u'),
):
    """Invoke a skill running locally or remotely"""
    if not secret:
        secret: str = typer.prompt('Secret', hide_input=True, type=str)
    while not len(secret) > 20:
        typer.echo('Secrets must be at least 20 characters')
        secret = typer.prompt('Secret', hide_input=True)

    if not public_key_path:
        public_key_path = Path(typer.prompt('Public key path', Path('./id_rsa.pub')))

    if not public_key_path.exists():
        while 1:
            typer.secho(f'The path {public_key_path} does not exist, please try again', color=typer.colors.RED)
            public_key_path = Path(typer.prompt('Public key path', public_key_path))
            if public_key_path.exists():
                break
    if not url:
        url = typer.prompt('URL to invoke the skill', default=url)

    public_key_text = public_key_path.read_text(encoding='utf-8')
    typer.echo('Enter commands below (Ctl+C to exit)')
    query = typer.prompt('>>', prompt_suffix=' ')

    challenge = os.urandom(16).hex()
    message = {
        'challenge': challenge,
        'text': query,
        'context': {},
        'params': {},
        'frame': {},
        'history': [],
    }
    while True:
        req = crypto.prepare_payload(json.dumps(message), public_key_text, secret)
        resp = requests.post(url, json=req)
        json_resp = resp.json()

        if not json_resp.get('challenge') == challenge:
            typer.secho('Skill did not respond with expected challenge value', fg=typer.colors.RED, err=True)

        typer.echo(pprint(json_resp, indent=2, width=120))
        query = typer.prompt('>>', prompt_suffix=' ')

        challenge = os.urandom(16).hex()
        message = {
            'challenge': challenge,
            'text': query,
            'context': json_resp.get('context', {}),
            'params': {},
            'frame': json_resp.get('frame'),
            'history': json_resp.get('history'),
        }


@app.command()
def generate_keys(
    filepath: Optional[Path] = typer.Argument(None),
    name: Optional[str] = 'id_rsa',
    use_password: Optional[bool] = typer.Option(False, '-p', help='Use a password for the private key'),
):
    """Generate an RSA keypair"""
    if not filepath:
        filepath = Path.cwd()

    typer.secho('🔐 Generating new RSA keypair...', fg=typer.colors.GREEN)

    if use_password:
        password: str = typer.prompt('Password', hide_input=True, confirmation_prompt=True)
        encryption = serialization.BestAvailableEncryption(password.encode('utf-8'))
    else:
        encryption = serialization.NoEncryption()

    priv_path = filepath / f'{name}.pem'
    pub_path = filepath / f'{name}.pub'

    if priv_path.exists() or pub_path.exists():
        confirmation = typer.confirm(f'File exists, would you like to overwrite the files at {priv_path}')
        if not confirmation:
            return
    typer.echo(f'Writing files {priv_path} and {pub_path} to {filepath.absolute()}')
    crypto.generate_keys(encryption, priv_path, pub_path)


@app.command()
def generate_secret():
    """Generate a secret token for signing requests"""
    typer.echo(secrets.token_urlsafe(16))


@app.command(name='new')
def new_skill(skill_name: str, secret: Optional[str] = None, password: Optional[str] = None):
    """Create a new skill project from a template"""
    # TODO: Support key generation, rather than making assumptions about its name
    # and location
    invoke_location = Path().resolve()
    package_location = Path(__file__).resolve()

    if not secret:
        secret = secrets.token_urlsafe(16)

    # Format the skill_name; Do not allow spaces
    skill_name = re.compile("[- ]+").sub('_', skill_name)

    # TODO: Add logic to use MM-less template when available
    template_path = package_location.parent / 'templates/mindmeld_template'

    rsa_filename: str = f'{skill_name}.id_rsa'
    cookiecutter(
        str(template_path),
        output_dir=str(invoke_location),
        no_input=True,
        extra_context={
            'skill_name': skill_name,
            'rsa_file_name': rsa_filename,  # Path to the RSA key
            'rsa_password': password,
            'app_secret': secret,
        },
    )

    Path(invoke_location / skill_name / skill_name / 'entities').mkdir()


def main():
    app()


if __name__ == '__main__':
    main()
