from __future__ import annotations
import logging
from typing import TYPE_CHECKING

from tqdm import tqdm
import typer

from webex_assistant_skills_sdk.supress_warnings import suppress_warnings

if TYPE_CHECKING:
    from mindmeld.components.nlp import NaturalLanguageProcessor


def init_mindmeld_nlp(app_path: str = '.') -> NaturalLanguageProcessor:
    try:
        with suppress_warnings():
            from mindmeld import configure_logs
            from mindmeld.components.nlp import NaturalLanguageProcessor
    except ImportError:
        typer.echo('You must install the extras package webex-assistant-sdk[mindmeld] to use NLP commmands')
        raise typer.Exit(1)

    configure_logs(level=logging.ERROR)
    progress_bar = tqdm(total=0, desc="NLP progress")

    return NaturalLanguageProcessor(app_path=app_path, progress_bar=progress_bar)
