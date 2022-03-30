from pydantic import BaseModel, Field


class DeviceContext(BaseModel):
    userId: str = Field(..., alias='user_id')
    orgId: str = Field(..., alias='org_id')
    deviceDeveloperId: str = Field(..., alias='device_developer_id')
