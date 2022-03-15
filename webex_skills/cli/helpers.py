import json
from pathlib import Path

import typer

from webex_skills.supress_warnings import suppress_warnings


def get_config_path() -> Path:
    """Returns the path of the config file for the app. Creates a config file if none exists."""
    app_dir = typer.get_app_dir('webex-skills', force_posix=True)
    config_path = Path(app_dir) / 'config.json'

    if not config_path.is_file():
        config_path.touch()

    return config_path


def get_config():
    config_path = get_config_path()
    config = json.loads(config_path.read_text(encoding='utf-8'))

def create_nlp(app_path):
    try:
        with suppress_warnings():
            from mindmeld.components.nlp import NaturalLanguageProcessor  # pylint:disable=import-outside-toplevel
    except ImportError as import_exc:
        error_text = 'You must install the extras package webex-assistant-sdk[mindmeld] to use NLP commmands'
        raise ImportError(error_text) from import_exc
    nlp = NaturalLanguageProcessor(app_path=app_path)
    return nlp
