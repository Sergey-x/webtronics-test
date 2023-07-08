from datetime import datetime

import factory
from models import Post
from tests.common import FACTORIES_SESSION


class PostsFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Post
        sqlalchemy_session = FACTORIES_SESSION
        sqlalchemy_session_persistence = "commit"

    @staticmethod
    def add(
            post_id: int,
            author_id: int,
            dt_created: datetime = datetime.now(),
            dt_updated: datetime | None = None,
            text: str = "content",
            likes: int = 0,
            is_available: bool = True,
    ):
        PostsFactory(
            id=post_id,
            dt_created=dt_created,
            dt_updated=dt_updated,
            text=text,
            author_id=author_id,
            likes=likes,
            is_available=is_available,
        )

        return {
            "id": post_id,
            "text": text,
            "dt_created": dt_created,
            "dt_updated": dt_updated,
            "author_id": author_id,
            "likes": likes,
            "is_available": is_available,
        }
