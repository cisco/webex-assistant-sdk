from __future__ import annotations
import json
from pathlib import Path
from typing import Dict, Optional

from pydantic import AnyHttpUrl, BaseModel, validator
import typer


class SkillConfig(BaseModel):
    name: str
    url: AnyHttpUrl
    secret: str 
    public_key: str

    @validator('url')
    def validate_url(cls, url: str):
        if not url.endswith('/parse'):
            return url + '/parse'

        return url


class CliConfig(BaseModel):
    skill_configs: Dict[str, SkillConfig] = {}

    @classmethod
    def from_file(cls) -> CliConfig:
        return cls.__load_config()

    def set_skill_config(self, skill_config: SkillConfig) -> None:
        self.skill_configs[skill_config.name] = skill_config

    def get_skill_config(self, skill_name: str) -> Optional[SkillConfig]:
        return self.skill_configs.get(skill_name, None)

    def save(self) -> None:
        config_path = self.__get_default_config_path()
        config_path.write_text(self.json(indent=2))

    @staticmethod
    def __get_default_config_path() -> Path:
        app_dir = Path(typer.get_app_dir('webex-skills', force_posix=True))
        config_path = app_dir / 'config.json'

        if not app_dir.exists():
            app_dir.mkdir(parents=True)

        if not config_path.is_file():
            config_path.touch()

        return config_path

    @classmethod
    def __load_config(cls) -> None:
        config_path = cls.__get_default_config_path()

        try:
            return cls.parse_file(
                config_path,
                content_type='application/json',
                encoding='utf8'
            )

        except json.JSONDecodeError:
            # ignore empty config
            pass

        return cls()
