from os import environ
from uuid import uuid4
from datetime import datetime, timedelta, timezone

from passlib.context import CryptContext

import jwt

from app.repositories import (
    UserRepository,
    DeviceRepository,
    RefreshTokenRepository,
)


PRIVATE_ACCESS_KEY = environ.get("PRIVATE_ACCESS_KEY")
PUBLIC_ACCESS_KEY = environ.get("PUBLIC_ACCESS_KEY")
PRIVATE_REFRESH_KEY = environ.get("PRIVATE_REFRESH_KEY")
PUBLIC_REFRESH_KEY = environ.get("PUBLIC_REFRESH_KEY")

pwd_context = CryptContext(
    schemes="argon2",
    argon2__rounds=3,
    argon2__memory_cost=65536,
    argon2__parallelism=4,
    argon2__type="id",
    deprecated="auto",
)


class AuthError(Exception):
    def __init__(self, details):
        self.details = details


class AuthService:
    @staticmethod
    def login(user, device_uuid, user_agent, last_ip, db) -> tuple[str, str, str]:
        if user_object := UserRepository(db).get_by_login(user.login):
            if not pwd_context.verify(user.password, user_object.password_hash):
                pass

            device_object = None

            if device_uuid is None:
                device_uuid = uuid4()
                device_object = DeviceRepository(db).add(user_object.id, device_uuid, user_agent, last_ip)
            else:
                device_object = DeviceRepository(db).get_by_uuid(device_uuid)

                if not device_object:
                    raise AuthError("Unknown device")

                device_object.last_ip = last_ip
                db.flush()

            access_token = AuthService.__create_access_token(user_object.id)
            refresh_token = AuthService.__create_refresh_token(user_object.id)

            RefreshTokenRepository(db).add(
                pwd_context.hash(refresh_token),
                device_object.id,
                datetime.now(timezone.utc) + timedelta(days=1),
            )

            db.commit()

            return [access_token, refresh_token, device_uuid]
        else:
            raise AuthError("Wrong password of login")

    @staticmethod
    def refresh(refresh_token, device_uuid, db) -> tuple[str, str]:
        device_obj = DeviceRepository(db).get_by_uuid(device_uuid)

        if device_obj is None:
            raise AuthError("Unknown device")

        verified_token_hash_id = None

        for refresh_token_obj in RefreshTokenRepository(db).get_device_tokens(
            device_obj.id
        ):
            if (
                pwd_context.verify(refresh_token, refresh_token_obj.token_hash)
                and not refresh_token_obj.revoked
            ):
                verified_token_hash_id = refresh_token_obj.id
                break

        if not verified_token_hash_id:
            raise AuthError("Unknown refresh token")

        payload = AuthService.__verify_refresh_token(refresh_token)

        access_token = AuthService.__create_access_token(payload["sub"])
        refresh_token = AuthService.__create_refresh_token(payload["sub"])

        RefreshTokenRepository(db).delete_device_tokens(verified_token_hash_id)
        RefreshTokenRepository(db).add(
            pwd_context.hash(refresh_token),
            device_obj.id,
            datetime.now(timezone.utc) + timedelta(hours=1),
        )

        db.commit()

        return [
            access_token,
            refresh_token,
        ]

    @staticmethod
    def logout(device_uuid, db) -> None:
        device_object = DeviceRepository(db).get_by_uuid(device_uuid)
        RefreshTokenRepository(db).delete_device_tokens(device_object.id)
        db.commit()

    @staticmethod
    def logout_device(device_id, db):
        DeviceRepository(db).delete(device_id)
        db.commit()

    @staticmethod
    def logout_all(user_id, db):
        devices = DeviceRepository(db).get_user_devices(user_id)
        for device in devices:
            DeviceRepository(db).delete(device.id)
        db.commit()

    @staticmethod
    def get_user(user_id, db):
        return UserRepository(db).get_by_id(user_id)

    @staticmethod
    def get_devices(device_uuid, user_id, db):
        devices = DeviceRepository(db).get_user_devices(user_id)
        for device in devices:
            if device.device_uuid == device_uuid:
                device.current_device = True
        return devices

    @staticmethod
    def get_tokens(device_uuid, db):
        device = DeviceRepository(db).get_by_uuid(device_uuid)
        return RefreshTokenRepository(db).get_device_tokens(device.id)

    @staticmethod
    def verify_token(token):
        if token:
            return jwt.decode(
                token,
                PUBLIC_ACCESS_KEY,
                "RS256",
            )
        else:
            raise AuthError("Missing token")

    @staticmethod
    def __verify_refresh_token(token):
        return jwt.decode(
            token,
            PUBLIC_REFRESH_KEY,
            "RS256",
        )

    @staticmethod
    def __create_access_token(user_id) -> str:
        return jwt.encode(
            {
                "sub": str(user_id),
                "exp": datetime.now(timezone.utc) + timedelta(minutes=1),
            },
            PRIVATE_ACCESS_KEY,
            algorithm="RS256",
        )

    @staticmethod
    def __create_refresh_token(user_id) -> str:
        return jwt.encode(
            {
                "sub": str(user_id),
                "exp": datetime.now(timezone.utc) + timedelta(days=1),
            },
            PRIVATE_REFRESH_KEY,
            algorithm="RS256",
        )
