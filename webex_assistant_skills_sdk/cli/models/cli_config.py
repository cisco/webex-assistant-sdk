from typing import Dict

from pydantic import AnyHttpUrl, BaseModel, validator


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
