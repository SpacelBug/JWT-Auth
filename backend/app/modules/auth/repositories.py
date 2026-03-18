from sqlalchemy import select

from app.db.repository import Repository

from app.modules.auth.models import User, Device, RefreshToken


class UserRepository(Repository):
    def get_by_id(self, user_id):
        return self.db.scalars(select(User).where(User.id == user_id)).one_or_none()

    def get_by_login(self, login):
        return self.db.scalars(select(User).where(User.login == login)).one_or_none()

    def add(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass


class ProfileRepository(Repository):
    def get(self):
        pass

    def add(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass


class DeviceRepository(Repository):

    def get_by_uuid(self, device_uuid):
        return self.db.scalars(
            select(Device).where(Device.device_uuid == device_uuid)
        ).one_or_none()

    def get_user_devices(self, user_id):
        return self.db.scalars(select(Device).where(Device.user_id == user_id)).all()

    def add(self, user_id, device_uuid, user_agent=None, last_ip=None):
        device_object = Device(
            user_id=user_id,
            device_uuid=device_uuid,
            user_agent=user_agent,
            last_ip=last_ip,
        )
        self.db.add(device_object)
        self.db.flush()
        return device_object

    def update(self):
        pass

    def delete(self, device_uuid):
        device_object = self.db.scalar(
            select(Device).where(Device.device_uuid == device_uuid)
        )
        self.db.delete(device_object)
        self.db.flush()


class RefreshTokenRepository(Repository):
    def get(self):
        pass

    def get_device_tokens(self, device_id) -> list[RefreshToken]:
        return self.db.scalars(
            select(RefreshToken).where(RefreshToken.device_id == device_id)
        ).all()

    def add(self, token_hash, device_id, expires_at):
        self.db.add(
            RefreshToken(
                device_id=device_id, token_hash=token_hash, expires_at=expires_at
            )
        )
        self.db.flush()

    def delete(self, token_id):
        self.db.delete(RefreshToken, token_id)
        self.db.flush()

    def delete_device_tokens(self, device_id):
        refresh_token_objects = self.db.scalars(
            select(RefreshToken).where(RefreshToken.device_id == device_id)
        ).all()
        for token_object in refresh_token_objects:
            self.db.delete(token_object)
        self.db.flush()

    def delete_user_tokens(self, user_id):
        refresh_token_objects = self.db.scalars(
            select(RefreshToken)
            .join(Device, Device.id == RefreshToken.device_id)
            .where(Device.user_id == user_id)
        ).all()
        for token_object in refresh_token_objects:
            self.db.delete(token_object)
        self.db.flush()
