import factory
from models import User
from tests.common import FACTORIES_SESSION
from utils.crypto import get_password_hash


class UsersFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = FACTORIES_SESSION
        sqlalchemy_session_persistence = "commit"

    @staticmethod
    def add(user_id: int, email: str, password: str = get_password_hash("password")):
        UsersFactory(id=user_id, email=email, password=password)

        return {
            "id": user_id,
            "email": email,
            "password": password,
        }
