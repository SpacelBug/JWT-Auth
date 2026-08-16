from sqlalchemy import Column, String, BigInteger, DateTime, Boolean, ForeignKey, func

from app.db.base import Base


class Device(Base):
    __tablename__ = "devices"
    __table_args__ = {"schema": "auth"}
    id = Column(BigInteger, primary_key=True)
    user_id = Column(
        BigInteger,
        ForeignKey("auth.users.id"),
        nullable=False,
    )
    device_uuid = Column(String, nullable=False)
    name = Column(String)
    user_agent = Column(String)
    last_ip = Column(String)
    created_at = Column(DateTime, nullable=False, default=func.now())
    last_seen_at = Column(DateTime)
