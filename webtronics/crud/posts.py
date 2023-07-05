import sqlalchemy as sa
from fastapi_pagination.ext.sqlalchemy import paginate
from models import Post
from schemas import CreatePostRequestSchema, PostResponseItem, UpdatePostRequestSchema
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import NoResultFound, OperationalError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func


class PostCRUD:
    @classmethod
    async def get_recent_posts(
            cls,
            db: AsyncSession,
    ) -> list | None:
        """Получить спсиок постов.

        Есть пагинация на уровне db.
        """
        select_stmt = (
            sa.select(Post)
            .where(Post.is_available == True)  # noqa
            .order_by(Post.dt_created)
        )

        try:
            return await paginate(db, select_stmt)
        except OperationalError:
            return []

    @classmethod
    async def get_post_by_id(
            cls,
            post_id: int,
            db: AsyncSession,
    ) -> PostResponseItem | None:
        """Получение поста с идентификатором `post_id`."""
        select_stmt = (
            sa.select(*Post.get_post_fields()).where(
                sa.and_(
                    Post.id == post_id,
                    Post.is_available == True,  # noqa
                )
            )
        )

        try:
            res = (await db.execute(select_stmt)).one()
            return PostResponseItem.parse_obj(dict(zip(Post.get_post_fields_keys(), res)))
        except NoResultFound:
            return None
        except OperationalError:
            return None

    @classmethod
    async def create_post(
            cls,
            db: AsyncSession,
            new_post_data: CreatePostRequestSchema,
            author_id: int,
    ) -> PostResponseItem | None:
        """Добавление в базу данных нового поста."""
        insert_stmt = (
            insert(Post)
            .values(text=new_post_data.text, author_id=author_id)
            .returning(*Post.get_post_fields())
        )

        try:
            res = (await db.execute(insert_stmt)).one_or_none()
            await db.commit()
            return PostResponseItem.parse_obj(dict(zip(Post.get_post_fields_keys(), res)))
        except OperationalError:
            return None

    @classmethod
    async def update_post(
            cls,
            db: AsyncSession,
            post_id: int,
            author_id: int,
            updated_post: UpdatePostRequestSchema,
    ) -> PostResponseItem | None:
        """Обновить пост с идентификатором `post_id`."""
        update_stmt = (
            sa.update(Post)
            .values(
                dt_updated=func.current_timestamp(),
                text=updated_post.text,
            )
            .where(
                sa.and_(
                    Post.id == post_id,
                    Post.author_id == author_id,
                    Post.is_available == True,  # noqa
                )
            )
            .returning(*Post.get_post_fields())
        )
        try:
            res = (await db.execute(update_stmt)).one()
            await db.commit()
            return PostResponseItem.parse_obj(dict(zip(Post.get_post_fields_keys(), res)))
        except NoResultFound:
            return None
        except OperationalError:
            return None

    @classmethod
    async def delete_post(
            cls,
            post_id: int,
            author_id: int,
            db: AsyncSession,
    ) -> int:
        """Удалить пост с идентификатором `post_id`.

        В действительности из базы пост не удаляется - он помечается недоступным.
        И в дальнейшем не учавствует в выдаче.
        Удалить может только автор.
        """
        soft_delete_stmt = (
            sa.update(Post)
            .values(is_available=False)
            .where(
                sa.and_(
                    Post.id == post_id,
                    Post.author_id == author_id,
                )
            )
        )
        res = (await db.execute(soft_delete_stmt)).rowcount  # noqa
        await db.commit()
        return res
