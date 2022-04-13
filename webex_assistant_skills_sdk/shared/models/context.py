from __future__ import annotations
from typing import List
from uuid import UUID

from pydantic import BaseModel, Field


class DeviceContext(BaseModel):
    userId: UUID = Field(..., alias='user_id')
    userType: str = Field(..., alias='user_type')
    orgId: UUID = Field(..., alias='org_id')
    deviceDeveloperId: UUID = Field(..., alias='device_developer_id')
    supportedDirectives: List[str] = Field(..., alias='supported_directives')

    @staticmethod
    def construct_default_context() -> DeviceContext:
        return DeviceContext(
            user_id=UUID('91724fe7-a05e-4067-b415-4c0abd51db3e'),
            user_type='user',
            org_id=UUID('44a93aa7-4f67-41ce-b0b6-28ea60c2999a'),
            device_developer_id=UUID('6f49a05b-ce92-4679-88e6-e79326adbabb'),
            supported_directives=[],
        )

    class Config:
        allow_population_by_field_name = True
