import typer

from .crypto import app as crypto_app
from .nlp import app as nlp_app
from .project import app as project_app
from .remote import remote as remote_app
from .skill import app as skill_app

app = typer.Typer()

app.add_typer(skill_app, name="skills")
app.add_typer(crypto_app, name="crypto")
app.add_typer(nlp_app, name='nlp')
app.add_typer(project_app)
app.add_typer(remote_app)


def main():
    app()


if __name__ == '__main__':
    main()
