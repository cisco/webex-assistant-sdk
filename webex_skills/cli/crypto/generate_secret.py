import typer

from webex_skills import crypto
from webex_skills.cli.crypto.app import crypto_app


@crypto_app.command()
def generate_secret():
    """Generate a secret token for signing requests"""
    typer.echo(crypto.generate_secret())
