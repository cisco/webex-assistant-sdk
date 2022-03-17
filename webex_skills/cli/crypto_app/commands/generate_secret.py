import typer

from webex_skills import crypto
from webex_skills.cli.crypto_app.app import app


@app.command()
def generate_secret() -> None:
    """Generate a secret token for signing requests"""
    typer.echo(crypto.generate_secret())
