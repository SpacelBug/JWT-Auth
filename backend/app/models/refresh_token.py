from sqlalchemy import Column, String, BigInteger, DateTime, Boolean, ForeignKey, func

from app.db.base import Base


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    __table_args__ = {"schema": "auth"}
    id = Column(BigInteger, primary_key=True)
    device_id = Column(
        BigInteger,
        ForeignKey("auth.devices.id"),
        nullable=False,
    )
    token_hash = Column(String)
    expires_at = Column(DateTime, nullable=False)
    revoked = Column(Boolean, default=False)
    created_at = Column(DateTime, nullable=False, default=func.now())