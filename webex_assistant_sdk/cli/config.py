import json
from pathlib import Path

import typer


def get_skill_config(name=None):
    app_dir = Path(typer.get_app_dir('skills-cli', force_posix=True))
    config_file = app_dir / 'config.json'

    if not app_dir.exists():
        typer.echo('Creating default configuration')
        app_dir.mkdir(parents=True)
        config = {}
    else:
        config = json.loads(config_file.read_text('utf-8')) or {}

    remotes = config.get('remotes', {})
    if not name:
        return remotes

    remote_config = remotes.get(name)
    if not remote_config:
        typer.secho(f'No configured remote with the name {name} found', color=typer.colors.RED, err=True)
        raise typer.Exit(1)

    return remote_config
