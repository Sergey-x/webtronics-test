import fastapi as fa
from httpx import AsyncClient, Response
from tests.conftest import AuthedUser, make_auth_header
from tests.factories.likes import LikesFactory
from tests.factories.posts import PostsFactory
from tests.factories.users import UsersFactory


class TestRemoveLike:
    @classmethod
    def get_url(cls, post_id: int) -> str:
        return f"/posts/{post_id}/like"

    async def test_remove_like_from_not_existing_post(self, async_client: AsyncClient, authed_user: AuthedUser):
        """Удаление лайка посту с несуществующем id."""
        response: Response = await async_client.delete(
            url=self.get_url(1234),
            headers=make_auth_header(authed_user.access_token),
        )
        assert response.status_code == fa.status.HTTP_400_BAD_REQUEST

    async def test_remove_like_from_deleted_post(self, async_client: AsyncClient, authed_user: AuthedUser):
        """Удаление лайка удаленному посту."""
        # создаем пользователя и его пост
        another_user = UsersFactory.add(
            user_id=authed_user.id + 1,
            email="firstname2.secondname@domain.com",
        )
        post_id = 1
        post = PostsFactory.add(post_id=post_id, author_id=another_user["id"], is_available=False, likes=1)

        # добавляем лайк
        LikesFactory.add(user_id=authed_user.id, post_id=post_id)

        # проверяем, что лайк удален
        response: Response = await async_client.delete(
            url=self.get_url(post["id"]),
            headers=make_auth_header(authed_user.access_token),
        )
        assert response.status_code == fa.status.HTTP_204_NO_CONTENT

    async def test_remove_like_from_own_post(self, async_client: AsyncClient, authed_user: AuthedUser):
        """Удаление лайка своему собственному посту."""
        post = PostsFactory.add(post_id=1, author_id=authed_user.id)
        response: Response = await async_client.delete(
            url=self.get_url(post["id"]),
            headers=make_auth_header(authed_user.access_token),
        )
        assert response.status_code == fa.status.HTTP_400_BAD_REQUEST

    async def test_remove_like_from_own_deleted_post(self, async_client: AsyncClient, authed_user: AuthedUser):
        """Удаление лайка своему собственному удаленному посту."""
        post = PostsFactory.add(post_id=1, author_id=authed_user.id, is_available=False)
        response: Response = await async_client.delete(
            url=self.get_url(post["id"]),
            headers=make_auth_header(authed_user.access_token),
        )
        assert response.status_code == fa.status.HTTP_400_BAD_REQUEST

    async def test_remove_like_from_other_post(self, async_client: AsyncClient, authed_user: AuthedUser):
        """Удаление лайка чужому посту."""
        # создаем нового пользователя и его пост с лайком
        another_user = UsersFactory.add(
            user_id=authed_user.id + 1,
            email="firstname2.secondname@domain.com",
        )
        post_id = 1
        PostsFactory.add(post_id=post_id, author_id=another_user["id"], likes=0)
        LikesFactory.add(post_id=post_id, user_id=authed_user.id)

        response: Response = await async_client.delete(
            url=self.get_url(post_id),
            headers=make_auth_header(authed_user.access_token),
        )
        assert response.status_code == fa.status.HTTP_204_NO_CONTENT

        # Проверяем, что триггер сработал и счетчик изменился
        response: Response = await async_client.get(
            url=f"/posts/{post_id}",
            headers=make_auth_header(authed_user.access_token),
        )
        assert response.json()["likes"] == 0
