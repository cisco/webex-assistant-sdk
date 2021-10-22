from pathlib import Path
from typing import Optional

from cryptography.hazmat.primitives import serialization
import typer
from webex_skills import crypto

app = typer.Typer()


@app.command()
def generate_keys(
    filepath: Optional[Path] = typer.Argument(
        None, help="The path where to save the keys created. By default, they get created in the current directory."
    ),
    name: Optional[str] = typer.Option('id_rsa', help="The name to use for the keys created."),
):
    """Generate an RSA keypair"""
    if not filepath:
        filepath = Path.cwd()

    typer.secho('🔐 Generating new RSA keypair...', fg=typer.colors.GREEN)

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
