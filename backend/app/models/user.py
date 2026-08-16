from sqlalchemy import Column, String, BigInteger

from app.db.base import Base


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "auth"}

    id = Column(BigInteger, primary_key=True, nullable=False)
    login = Column(String, nullable=False)
    email = Column(String)
    password_hash = Column(String, nullable=False)
    status = Column(String, default="inactive", nullable=False)