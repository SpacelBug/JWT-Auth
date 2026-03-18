from sqlalchemy import Column, String, BigInteger, DateTime, Boolean, ForeignKey, func

from app.db.base import Base


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "auth"}

    id = Column(BigInteger, primary_key=True, nullable=False)
    login = Column(String, nullable=False)
    email = Column(String)
    password_hash = Column(String, nullable=False)
    status = Column(String, default="inactive", nullable=False)


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
