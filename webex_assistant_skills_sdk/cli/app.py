from webex_assistant_skills_sdk.cli import base_app
from webex_assistant_skills_sdk.cli import crypto_app
from webex_assistant_skills_sdk.cli import nlp_app
from webex_assistant_skills_sdk.cli.container import *


app = base_app.app

app.add_typer(crypto_app.app)
app.add_typer(nlp_app.app)
