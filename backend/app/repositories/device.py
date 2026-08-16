from sqlalchemy import select

from app.db.repository import Repository
from app.models.device import Device


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

    def delete(self, device_id):
        device_object = self.db.scalar(
            select(Device).where(Device.id == device_id)
        )
        self.db.delete(device_object)
        self.db.flush()

    def delete_by_uuid(self, device_uuid):
        device_object = self.db.scalar(
            select(Device).where(Device.device_uuid == device_uuid)
        )
        self.db.delete(device_object)
        self.db.flush()