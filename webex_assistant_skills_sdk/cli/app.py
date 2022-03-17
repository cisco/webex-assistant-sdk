from dependency_injector import containers

from webex_assistant_skills_sdk.cli import base_app
from webex_assistant_skills_sdk.cli import crypto_app
from webex_assistant_skills_sdk.cli import nlp_app
from webex_assistant_skills_sdk.cli.container import populate_container


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
