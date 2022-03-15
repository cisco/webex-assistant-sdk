import typer

from webex_skills import __version__
from webex_skills.cli.base import app
from webex_skills.cli.crypto import app as crypto_app
from webex_skills.cli.nlp import app as nlp_app


app.add_typer(crypto_app, name="crypto")
app.add_typer(nlp_app, name='nlp')

def version_callback(show_version: bool) -> None:
    if show_version:
        typer.echo(__version__)
        raise typer.Exit()

@app.callback()
def main(
    _: bool = typer.Option(False, '--version', callback=version_callback, is_eager=True, show_default=False)
) -> None:
    """
    A CLI for creating, managing, and testing Webex Assistant Skills
    """

if __name__ == '__main__':
    app()
