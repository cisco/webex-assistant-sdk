from webex_skills.cli.base import base_app
from webex_skills.cli.crypto import crypto_app
from webex_skills.cli.nlp import nlp_app


base_app.add_typer(crypto_app, name="crypto")
base_app.add_typer(nlp_app, name='nlp')
