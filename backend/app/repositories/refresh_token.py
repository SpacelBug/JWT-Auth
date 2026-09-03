from sqlalchemy import select, delete

from app.db.repository import Repository
from app.models.refresh_token import RefreshToken
from app.models.device import Device


class RefreshTokenRepository(Repository):
    def get(self):
        return self.db.scalars(select(RefreshToken)).all()

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

    def delete_device_tokens(self, device_id) -> int:
        res = self.db.execute(
            delete(RefreshToken).where(RefreshToken.device_id == device_id)
        )
        self.db.flush()
        return res.rowcount

    def delete_user_tokens(self, user_id):
        refresh_token_objects = self.db.scalars(
            select(RefreshToken)
            .join(Device, Device.id == RefreshToken.device_id)
            .where(Device.user_id == user_id)
        ).all()
        for token_object in refresh_token_objects:
            self.db.delete(token_object)
        self.db.flush()
