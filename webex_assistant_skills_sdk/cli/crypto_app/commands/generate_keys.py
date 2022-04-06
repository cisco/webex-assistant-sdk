from pathlib import Path

from dependency_injector.wiring import Provide
import typer

from webex_assistant_skills_sdk.cli.crypto_app.app import app
from webex_assistant_skills_sdk.cli.shared.services import CryptoGenService
from webex_assistant_skills_sdk.cli.types import Types


__crypto_gen_service: CryptoGenService = Provide[Types.CRYPTO_SERVICE]

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

    __crypto_gen_service.generate_keys(private_key_path, public_key_path)

    typer.echo(f'Done! {private_key_name} and {public_key_name} written to {directory_path}')
