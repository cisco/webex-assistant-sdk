from webex_assistant_skills_sdk.cli.nlp_app.app import app
from webex_assistant_skills_sdk.cli.helpers import init_mindmeld_nlp


@app.command()
def build() -> None:
    """Build nlp models associated with this skill"""
    nlp = init_mindmeld_nlp()
    nlp.build()
