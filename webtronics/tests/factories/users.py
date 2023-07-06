import factory
from models import User
from tests.common import FACTORIES_SESSION


class UsersFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = FACTORIES_SESSION
        sqlalchemy_session_persistence = "commit"

    @staticmethod
    def add(user_id: int, email: str, password: str):
        UsersFactory(id=user_id, email=email, password=password)

        return {
            "id": user_id,
            "email": email,
            "password": password,
        }
