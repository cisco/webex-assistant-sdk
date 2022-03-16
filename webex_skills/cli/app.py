from dependency_injector import containers

from webex_skills.cli import base_app
from webex_skills.cli import crypto_app
from webex_skills.cli import nlp_app
from webex_skills.cli.container import populate_container


app = base_app.app

app.add_typer(crypto_app.app)
app.add_typer(nlp_app.app)

container = containers.DynamicContainer()

populate_container(container)

container.wire(packages=[
    base_app,
    crypto_app,
    nlp_app,
])
