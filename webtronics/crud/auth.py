import sqlalchemy as sa
from models import User
from schemas.auth import SignInRequestSchema, SignUpRequestSchema
from sqlalchemy.exc import IntegrityError, NoResultFound, OperationalError
from sqlalchemy.ext.asyncio import AsyncSession
from utils.crypto import get_password_hash, verify_password


class AuthCRUD:
    @classmethod
    async def get_user_id_by_creds(
            cls,
            db: AsyncSession,
            user_creds: SignInRequestSchema,
    ) -> int | None:
        """Получить идентификатор пользователя по почте и паролю."""
        select_stmt = (
            sa.select(User.id, User.password).where(
                sa.and_(
                    User.email == user_creds.email,  # noqa
                )
            )
        )
        try:
            res = (await db.execute(select_stmt)).one()
            is_good_creds: bool = verify_password(user_creds.password, res[1])
            if is_good_creds:
                return res[0]
            return None
        except NoResultFound:
            return None
        except OperationalError:
            return None

    @classmethod
    async def sign_up(
            cls,
            db: AsyncSession,
            user_creds: SignUpRequestSchema,
    ) -> int | None:
        """Добавление в базу нового пользователя."""
        hashed_psw: str = get_password_hash(user_creds.password)

        insert_stmt = (
            sa.insert(User)
            .values(
                email=user_creds.email.lower(),
                password=hashed_psw,
            )
            .returning(User.id)
        )

        try:
            res = (await db.execute(insert_stmt)).scalar()
            await db.commit()
            return res
        except IntegrityError:
            return None
        except OperationalError:
            return None
