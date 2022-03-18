from dependency_injector.wiring import Provide
import typer

from webex_assistant_skills_sdk import crypto
from webex_assistant_skills_sdk.cli.crypto_app.app import app
from webex_assistant_skills_sdk.cli.shared.services import CliCryptoService
from webex_assistant_skills_sdk.cli.types import Types


__crypto_service: CliCryptoService = Provide[Types.CLI_CRYPTO_SERVICE]

@app.command()
def generate_secret() -> None:
    """Generate a secret token for signing requests"""
    typer.echo(__crypto_service.generate_secret())
