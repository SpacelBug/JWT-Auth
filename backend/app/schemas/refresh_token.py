from datetime import datetime
from pydantic import BaseModel


class RefreshTokenResponse(BaseModel):
    created_at: datetime
    expires_at: datetime
    revoked: bool
