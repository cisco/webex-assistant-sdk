import json
from pathlib import Path
from typing import List, Optional

import typer

from webex_skills.cli.models import CliConfig, SkillConfig


class CliConfigService():
    config_: CliConfig

    def __init__(self) -> None:
        self.config_ = self.__load_config()

    def set_skill_config(self, skill_config: SkillConfig) -> None:
        self.config_.skill_configs[skill_config.name] = skill_config

    def delete_skill_config(self, skill_name: str) -> None:
        del self.config_.skill_configs[skill_name]

    def get_skill_names(self) -> List[str]:
        return self.config_.skill_configs.keys()

    def get_skill_config(self, skill_name: str) -> Optional[SkillConfig]:
        return self.config_.skill_configs.get(skill_name, None)

    def save_config(self) -> None:
        config_path = self.__get_default_config_path()
        config_path.write_text(self.config_.json(indent=2))

    def __get_default_config_path(self) -> Path:
        app_dir = Path(typer.get_app_dir('webex-skills', force_posix=True))
        config_path = app_dir / 'config.json'

        if not app_dir.exists():
            app_dir.mkdir(parents=True)

        if not config_path.is_file():
            config_path.touch()

        return config_path

    def __load_config(self) -> None:
        config_path = self.__get_default_config_path()

        try:
            return CliConfig.parse_file(
                config_path,
                content_type='application/json',
                encoding='utf8'
            )

        except json.JSONDecodeError:
            # ignore empty config
            pass

        return CliConfig()
