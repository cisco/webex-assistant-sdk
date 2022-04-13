from __future__ import annotations

from pathlib import Path
from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    skill_name: Optional[str]
    private_key_path: Path = 'id_rsa.pem'
    secret: Optional[str]
    use_encryption: bool = True
    log_level: str = 'INFO'
    app_dir: Optional[str] = None
    
    @staticmethod
    def construct_default_test_settings() -> Settings:
        return Settings(
            use_encryption=False,
        )

    class Config:
        env_prefix = 'SKILLS_'
        env_file = '.env'
