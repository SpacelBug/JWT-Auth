from sqlalchemy import select

from app.db.repository import Repository
from app.models.user import User


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