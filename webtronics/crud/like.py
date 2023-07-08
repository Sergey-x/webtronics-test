import sqlalchemy as sa
from models import Post, PostLike
from sqlalchemy.exc import IntegrityError, OperationalError

from .base import BaseCRUD


class PostLikeCRUD(BaseCRUD):

    @classmethod
    async def add_like(cls, post_id: int, user_id: int) -> int:
        """Добавить лайк."""
        is_own_post_sql = sa.select(Post.id).where(
            sa.or_(
                sa.and_(
                    Post.id == post_id,
                    Post.author_id == user_id,
                ),
                Post.is_available == False,  # noqa
            )

        ).exists()

        insert_like_stmt = (
            sa.insert(PostLike)
            .from_select(
                ["user_id", "post_id"],
                sa.select(user_id, post_id).where(is_own_post_sql == False),  # noqa
            )
        )

        # print(insert_like_stmt.compile(dialect=postgresql.dialect()))
        try:
            res = (await cls.execute(insert_like_stmt)).rowcount
            return res
        except IntegrityError:
            return 0
        except OperationalError:
            return 0

    @classmethod
    async def remove_like(cls, post_id: int, user_id: int) -> int:
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
            res: int = (await cls.execute(drop_like_stmt)).rowcount
            return res
        except IntegrityError:
            return 0
        except OperationalError:
            return 0
