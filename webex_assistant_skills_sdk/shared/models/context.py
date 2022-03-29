from pydantic import BaseModel, Field


class DeviceContext(BaseModel):
    user_id: str = Field(..., alias='userId')
    org_id: str = Field(..., alias='orgId')
    device_developer_id: str = Field(..., alias='deviceDeveloperId')
