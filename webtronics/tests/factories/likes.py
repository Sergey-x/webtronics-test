import factory
from models import PostLike
from tests.common import FACTORIES_SESSION


class LikesFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = PostLike
        sqlalchemy_session = FACTORIES_SESSION
        sqlalchemy_session_persistence = "commit"

    @staticmethod
    def add(post_id: int, user_id: int):
        LikesFactory(post_id=post_id, user_id=user_id)

        return {
            "post_id": post_id,
            "user_id": user_id,
        }
