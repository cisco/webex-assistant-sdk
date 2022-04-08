from typing import List
from uuid import UUID

from pydantic import BaseModel, Field


class DeviceContext(BaseModel):
    userId: UUID = Field(..., alias='user_id')
    userType: str = Field(..., alias='user_type')
    orgId: UUID = Field(..., alias='org_id')
    deviceDeveloperId: UUID = Field(..., alias='device_developer_id')
    supportedDirectives: List[str] = Field(..., alias='supported_directives')

    class Config:
        allow_population_by_field_name = True
