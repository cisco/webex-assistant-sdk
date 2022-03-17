import json
from pathlib import Path

import typer

CONFIG_DIR = Path(typer.get_app_dir('skills-cli', force_posix=True))
CONFIG_FILE = CONFIG_DIR / 'config.json'


def get_skill_config(name: str):
    """Return the configuration for a named skill"""
    remotes = get_remotes()
    return remotes.get(name)


def get_remotes():
    """Returns configuration for all named skills"""
    if not CONFIG_FILE.exists():
        return {}
    config = json.loads(CONFIG_FILE.read_text(encoding='utf-8'))
    return config.get('remotes', {})


def get_app_dir(name: str):
    """Returns the app directory path for a named skill"""
    config = get_skill_config(name)
    if not config:
        typer.secho(f'No configured remote with the name {name} found', color=typer.colors.RED, err=True)
        raise typer.Exit(1)
    return config['app_dir']
