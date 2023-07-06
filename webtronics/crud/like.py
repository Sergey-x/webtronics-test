import sqlalchemy as sa
from models import PostLike
from sqlalchemy.exc import IntegrityError, OperationalError

from .base import BaseCRUD


class PostLikeCRUD(BaseCRUD):

    @classmethod
    async def add_like(cls, post_id: int, user_id: int):
        """Добавить лайк."""
        insert_like_stmt = (
            sa.insert(PostLike).values(post_id=post_id, user_id=user_id)
        )

        try:
            res = await cls.execute(insert_like_stmt)
            return res
        except IntegrityError:
            return None
        except OperationalError:
            return None

    @classmethod
    async def remove_like(cls, post_id: int, user_id: int) -> int | None:
        """Убрать лайк."""
        drop_like_stmt = (
            sa.delete(PostLike)
            .where(
                sa.and_(
                    PostLike.post_id == post_id,
                    PostLike.user_id == user_id,
                )
            )
        )

        try:
            res = (await cls.execute(drop_like_stmt)).rowcount
            return res
        except IntegrityError:
            return None
        except OperationalError:
            return None
