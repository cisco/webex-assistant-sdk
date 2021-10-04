import json
from json import JSONDecodeError
import os
from pathlib import Path
from pprint import pformat
from typing import Optional

import requests
import typer
import uvicorn

from webex_assistant_sdk import crypto
from webex_assistant_sdk.cli.config import get_skill_config

app = typer.Typer()


# TODO: Make this more robust, handling various types of errors without completely shitting the bed
@app.command()
def invoke(
    name: Optional[str] = typer.Argument(None),
    secret: Optional[str] = typer.Option(None, '--secret', '-s'),
    public_key_path: Optional[Path] = typer.Option(None, '-k', '--key'),
    url: Optional[str] = typer.Option(None, '-u'),
    verbose: Optional[bool] = typer.Option(None, '-v'),
    encrypted: Optional[bool] = typer.Option(True, '--encrypt/--no-encrypt', is_flag=True),
):
    # TODO: better error handling for responses
    """Invoke a skill running locally or remotely"""
    if name:
        # Load details from config
        config = get_skill_config(name)
        url = url or config['url']
        public_key_path = public_key_path or Path(config['public_key_path'])
        secret = secret or config['secret']

    public_key_text = public_key_path.read_text(encoding='utf-8')
    typer.echo('Enter commands below (Ctl+C to exit)')
    query = typer.prompt('>>', prompt_suffix=' ')
    invoke_skill(query, url, encrypted, public_key_text, secret, verbose)


def invoke_skill(query, url, encrypted, public_key, secret, verbose=False):
    challenge = os.urandom(32).hex()
    message = {
        'challenge': challenge,
        'text': query,
        'context': {},
        'params': {
            'time_zone': 'sometime',
            'timestamp': 12345,
            'language': 'en',
        },
        'frame': {},
        'history': [],
    }

    while True:
        req = message
        if encrypted:
            req = crypto.prepare_payload(json.dumps(message), public_key, secret)

        resp = requests.post(url, json=req)

        if verbose:
            typer.secho(f'Sending Message: {pformat(req)}\n\n', fg=typer.colors.GREEN)

        if resp.status_code != 200:
            typer.secho(f'Skill responded with status code {resp.status_code}', fg=typer.colors.RED)

        try:
            json_resp = resp.json()
        except JSONDecodeError:
            typer.secho('Unable to deserialize JSON response')
            json_resp = {}

        # TODO: Handle non-200 responses or validation errors
        if not json_resp.get('challenge') == challenge:
            typer.secho('Skill did not respond with expected challenge value', fg=typer.colors.RED, err=True)

        typer.secho(pformat(json_resp, indent=2, width=120), fg=typer.colors.GREEN)
        query = typer.prompt('>>', prompt_suffix=' ')

        challenge = os.urandom(32).hex()
        message = {
            'challenge': challenge,
            'text': query,
            'context': json_resp.get('context', {}),
            'params': {
                'time_zone': 'sometime',
                'timestamp': 12345,
                'language': 'en',
            },
            'frame': json_resp.get('frame', []),
            'history': json_resp.get('history', []),
        }


@app.command()
def check():
    """Performs a health check on a given skill"""


@app.command()
def run(skill_name: str):
    skill_name = skill_name.replace('-', '_')
    uvicorn.run(f'{skill_name}.app:api', host="127.0.0.1", port=8080, log_level="info")
