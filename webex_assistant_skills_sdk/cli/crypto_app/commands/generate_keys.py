from pathlib import Path

from cryptography.hazmat.primitives import serialization
import typer

from webex_assistant_skills_sdk import crypto
from webex_assistant_skills_sdk.cli.crypto_app.app import app


@app.command()
def generate_keys(
    directory_path: Path = typer.Option(
        Path.cwd(),
        '--path',
        exists=True,
        dir_okay=True,
        file_okay=False,
        readable=True,
        writable=True,
        help="A path to the directory in which the keys will be generated."
    ),
    file_name: str = typer.Option(
        'id_rsa',
        '--name',
        help="The name to use for the generated keys."
    ),
) -> None:
    """Generate an RSA keypair"""
    encryption = serialization.NoEncryption()

    private_key_name = f'{file_name}.pem'
    private_key_path = directory_path / private_key_name

    public_key_name = f'{file_name}.pub'
    public_key_path = directory_path / public_key_name

    if private_key_path.exists() or public_key_path.exists():
        typer.confirm(
            (
                'RSA keypair already exists, would you like to overwrite '
                f'{private_key_name} and {public_key_name} in {directory_path}?'
            ),
            default=False,
            abort=True,
        )

    typer.echo('🔐 Generating new RSA keypair...')

    ## TODO: replace with service call
    crypto.generate_keys(private_key_path, public_key_path, encryption=encryption)

    typer.echo(f'Done! {private_key_name} and {public_key_name} written to {directory_path}')
