from typing import Dict

from pydantic import AnyHttpUrl, BaseModel


class SkillConfig(BaseModel):
    name: str
    url: AnyHttpUrl
    secret: str 
    public_key: str


class CliConfig(BaseModel):
    skill_configs: Dict[str, SkillConfig] = {}
