import typer

from webex_skills import __version__


base_app = typer.Typer()

def version_callback(show_version: bool) -> None:
    if show_version:
        typer.echo(__version__)
        raise typer.Exit()

@base_app.callback()
def app(
    _: bool = typer.Option(False, '--version', callback=version_callback, is_eager=True, show_default=False)
) -> None:
    """
    A CLI for creating, managing, and testing Webex Assistant Skills
    """
