import typer

from webex_skills import __version__


app = typer.Typer()

def version_callback(show_version: bool) -> None:
    if show_version:
        typer.echo(__version__)
        raise typer.Exit()

@app.callback()
def app_callback(
    _: bool = typer.Option(False, '--version', callback=version_callback, is_eager=True, show_default=False)
) -> None:
    """
    A CLI for creating, managing, and testing Webex Assistant Skills
    """
