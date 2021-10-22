from datetime import datetime
import json
from json import JSONDecodeError
import locale
import os
from pathlib import Path
from pprint import pformat
import sys
from typing import Optional

import requests
import typer
from typer import colors
import uvicorn

from ..crypto.messages import generate_token, prepare_payload
from ..crypto.signatures import sign_token
from .config import get_skill_config

app = typer.Typer()


@app.command()
def invoke(
    name: Optional[str] = typer.Argument(
        None,
        help="The name of the skill to invoke. If none specified, you would need to"
        " at least provide the `public_key_path` and `secret`. If specified, all"
        " following configuration (keys, secret, url, ect.) will be extracted"
        " from the skill.",
    ),
    secret: Optional[str] = typer.Option(
        None, '--secret', '-s', help="The secret for the skill. If none provided you will be asked for it."
    ),
    public_key_path: Optional[Path] = typer.Option(
        None, '-k', '--key', help="The path of the public key for the skill."
    ),
    url: Optional[str] = typer.Option(None, '-u', help="The public url for the skill."),
    verbose: Optional[bool] = typer.Option(None, '-v', help="Set this flag to get a more verbose output."),
    encrypted: Optional[bool] = typer.Option(
        True, '--encrypt/--no-encrypt', is_flag=True, help="Flag to specify if the skill is using encryption."
    ),
):
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
    default_params = {
        'time_zone': 'UTC',
        'timestamp': datetime.utcnow().timestamp(),
        'language': 'en',
    }
    message = {
        'challenge': challenge,
        'text': query,
        'context': {},
        'params': default_params,
        'frame': {},
        'history': [],
    }

    while True:
        req = message
        if encrypted:
            req = prepare_payload(json.dumps(message), public_key, secret)

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

        if not json_resp.get('challenge') == challenge:
            typer.secho('Skill did not respond with expected challenge value', fg=typer.colors.RED, err=True)

        typer.secho(pformat(json_resp, indent=2, width=120), fg=typer.colors.GREEN)
        query = typer.prompt('>>', prompt_suffix=' ')

        challenge = os.urandom(32).hex()
        message = {
            'challenge': challenge,
            'text': query,
            'context': json_resp.get('context', {}),
            'params': json_resp.get('params', default_params),
            'frame': json_resp.get('frame', []),
            'history': json_resp.get('history', []),
        }


@app.command()
def run(skill_name: str = typer.Argument(..., help="The name of the skill to run.")):
    config = get_skill_config(skill_name)
    sys.path.insert(0, config['project_path'])
    os.environ['SKILLS_PRIVATE_KEY_PATH'] = config['private_key_path']
    os.environ['SKILLS_SECRET'] = config['secret']
    os.environ['SKILLS_APP_DIR'] = config['app_dir']
    uvicorn.run(f'{skill_name}.main:api', host="127.0.0.1", port=8080, log_level="info")


@app.command()
def check(
    name: Optional[str] = typer.Argument(
        None,
        help="The name of the skill to check. If none specified, you would need to"
        " at least provide the `public_key_path` and `secret`. If specified, all"
        " following configuration (keys, secret, etc.) will be extracted"
        " from the skill.",
    ),
    secret: Optional[str] = typer.Option(
        None, '--secret', '-s', help="The secret for the skill. If none provided you will be asked for it."
    ),
    public_key_path: Optional[Path] = typer.Option(
        None, '-k', '--key', help="The path of the public key for the skill."
    ),
    url: Optional[str] = typer.Option('http://localhost:8080/check', '-u', help="The check url for the skill."),
):
    if name:
        # Load details from config
        config = get_skill_config(name)
        public_key_path = public_key_path or Path(config['public_key_path'])
        secret = secret or config['secret']

    public_key_text = public_key_path.read_text(encoding='utf-8')
    challenge = os.urandom(32).hex()
    token = generate_token(challenge, public_key_text)
    signature = sign_token(token, secret)

    resp = requests.get(url, params={'signature': signature, 'message': token})
    if resp.status_code != 200:
        typer.secho(f'Non-200 response from skill: {resp.content}', fg=colors.RED)
        return

    try:
        json_resp = resp.json()
    except JSONDecodeError:
        typer.secho(f'Invalid json response {resp.content}', fg=colors.RED)
        return

    resp_challenge = json_resp.get('challenge')
    if not resp_challenge or resp_challenge != challenge:
        typer.secho(f'Invalid challenge response {resp_challenge}', fg=colors.RED)
        return

    typer.secho(f'{name} appears to be working correctly', fg=colors.GREEN)
