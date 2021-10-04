from pathlib import Path
from typing import Optional

from pydantic import BaseSettings


class SkillSettings(BaseSettings):
    skill_name: str
    private_key_path: Path = 'id_rsa.pem'
    secret: str
    use_encryption: bool = True
    log_level: str = 'INFO'
    app_dir: Optional[str] = None
    mindmeld: bool = False

    class Config:
        env_prefix = 'SKILLS_'
        env_file = '.env'
