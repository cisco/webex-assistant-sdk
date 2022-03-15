from pathlib import Path

import typer

from webex_skills.cli.config_models import CliConfig, SkillConfig
from webex_skills.crypto import generate_secret


app = typer.Typer()

def add_validate_skill_name(ctx: typer.Context, skill_name: str):
    if ctx.resilient_parsing:
        return

    cli_config = CliConfig.from_file()
    if skill_name in cli_config.skill_configs.keys():
        raise typer.BadParameter(f'A skill with name "{skill_name}" already exists')

@app.command()
def add(
    name: str = typer.Argument(
        ...,
        help='The name of the skill',
        callback=add_validate_skill_name
    ),
    url: str = typer.Option(
        'http://localhost:8080/parse',
        prompt=True,
        help='The URL of the skill',
    ),
    secret: str = typer.Option(
        None,
        envvar='SKILLS_SECRET',
        show_envvar=False,
        prompt=True,
        help='The skill secret',
    ),
    public_key_path: Path = typer.Option(
        Path.cwd() / 'id_rsa.pem',
        '--key',
        prompt=True,
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        help='The path to the public key',
    ),
):
    '''Add the configuration for a skill'''
    cli_config = CliConfig.from_file()

    public_key = public_key_path.read_text()

    skill_config = SkillConfig(
        name=name,
        url=url,
        secret=secret,
        public_key='blah',
    )
    cli_config.set_skill_config(skill_config)

    cli_config.save()
    

@app.command()
def check():
    pass

@app.command()
def delete():
    pass

@app.command()
def edit():
    pass

@app.command()
def init():
    pass

@app.command()
def invoke():
    pass

@app.command()
def list():
    pass

@app.command()
def view():
    pass
