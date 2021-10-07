from pathlib import Path
from typing import Optional

from cryptography.hazmat.primitives import serialization
import typer

from webex_assistant_sdk import crypto

app = typer.Typer()


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
    crypto.generate_keys(priv_path, pub_path, encryption=encryption)


@app.command()
def generate_secret():
    """Generate a secret token for signing requests"""
    typer.echo(crypto.generate_secret())