from pathlib import Path

from dependency_injector.wiring import Provide
import typer

from webex_assistant_skills_sdk.cli.crypto_app.app import app
from webex_assistant_skills_sdk.cli.shared.services import CryptoGenService
from webex_assistant_skills_sdk.cli.types import Types


_crypto_gen_service: CryptoGenService = Provide[Types.CRYPTO_SERVICE]

@app.command()
def generate_keys(
    key_path: Path = typer.Option(
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
    _crypto_gen_service.generate_keys(
        key_path,
        file_name,
        confirm=True,
    )
