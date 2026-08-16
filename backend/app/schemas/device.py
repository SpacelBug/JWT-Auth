from datetime import datetime
from pydantic import BaseModel


class DeviceResponse(BaseModel):
    id: int
    current_device: bool | None = False
    name: str | None = None
    user_agent: str | None = None
    last_ip: str | None = None
    created_at: datetime
    last_seen_at: datetime | None = None
