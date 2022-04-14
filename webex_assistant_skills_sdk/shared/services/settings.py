from __future__ import annotations

from pathlib import Path
from typing import Optional

from pydantic import BaseSettings as PydanticBaseSettings


class BaseSettings:
    skill_name: Optional[str] = None
    private_key_path: Path = 'id_rsa.pem'
    secret: Optional[str] = None
    use_encryption: bool = True
    log_level: str = 'INFO'
    app_dir: Optional[str] = None


class Settings(PydanticBaseSettings, BaseSettings):
    class Config:
        env_prefix = 'SKILLS_'
        env_file = '.env'
