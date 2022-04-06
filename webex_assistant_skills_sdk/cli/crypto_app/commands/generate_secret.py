import typer

from dependency_injector.wiring import Provide

from webex_assistant_skills_sdk.cli.crypto_app.app import app
from webex_assistant_skills_sdk.cli.shared.services import CryptoGenService
from webex_assistant_skills_sdk.cli.types import Types


__crypto_gen_service: CryptoGenService = Provide[Types.CRYPTO_SERVICE]

@app.command()
def generate_secret() -> None:
    """Generate a secret token for signing requests"""
    typer.echo(__crypto_gen_service.generate_secret())
