from datetime import datetime
from pydantic import BaseModel


class RefreshTokenResponse(BaseModel):
    id: int
    device_id: int
    created_at: datetime
    expires_at: datetime
    revoked: bool
