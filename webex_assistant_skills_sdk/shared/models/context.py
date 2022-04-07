from typing import List
from uuid import UUID

from pydantic import BaseModel, Field


class DeviceContext(BaseModel):
    userId: UUID = Field(..., alias='user_id')
    orgId: UUID = Field(..., alias='org_id')
    deviceDeveloperId: UUID = Field(..., alias='device_developer_id')
    supportedDirectives: List[str] = Field(..., alias='supported_directives')
