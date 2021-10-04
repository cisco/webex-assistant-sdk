import typer

app = typer.Typer(help='Commands for working with NLP models')


def create_nlp(app_path):
    try:
        from mindmeld.components.nlp import NaturalLanguageProcessor
    except ImportError:
        raise ImportError('You must install the extras package webex-assistant-sdk[mindmeld] to use NLP commmands')
    # TODO: Add root command to handle import and initialization of NLP processor or whatever
    # so that we don't import mindmeld unless and until we actually need it

    nlp = NaturalLanguageProcessor(app_path=app_path)
    return nlp


@app.command()
def build(app_path):
    """Build nlp models associated with this skill"""


@app.command()
def initialize():
    """Create initial structure for mindmeld models"""
    # TODO: Add option to augment data


@app.command()
def process():
    """Run a query through NLP processing"""
