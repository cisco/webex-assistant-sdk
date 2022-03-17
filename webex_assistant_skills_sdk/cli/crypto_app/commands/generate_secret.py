import typer

from webex_assistant_skills_sdk import crypto
from webex_assistant_skills_sdk.cli.crypto_app.app import app


@app.command()
def generate_secret() -> None:
    """Generate a secret token for signing requests"""
    typer.echo(crypto.generate_secret())
