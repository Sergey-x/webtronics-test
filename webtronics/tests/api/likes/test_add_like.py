import fastapi as fa
from httpx import AsyncClient, Response
from tests.conftest import AuthedUser, make_auth_header
from tests.factories.posts import PostsFactory
from tests.factories.users import UsersFactory


class TestAddLike:
    @classmethod
    def get_url(cls, post_id: int) -> str:
        return f"/posts/{post_id}/like"

    async def test_add_like_to_not_existing_post(self, async_client: AsyncClient, authed_user: AuthedUser):
        """Добавление лайка посту с несуществующем id."""
        response: Response = await async_client.post(
            url=self.get_url(1234),
            headers=make_auth_header(authed_user.access_token),
        )
        assert response.status_code == fa.status.HTTP_400_BAD_REQUEST

    async def test_add_like_to_deleted_post(self, async_client: AsyncClient, authed_user: AuthedUser):
        """Добавление лайка удаленному посту."""
        another_user = UsersFactory.add(
            user_id=authed_user.id + 1,
            email="firstname2.secondname@domain.com",
        )
        post = PostsFactory.add(post_id=1, author_id=another_user["id"], is_available=False)
        response: Response = await async_client.post(
            url=self.get_url(post["id"]),
            headers=make_auth_header(authed_user.access_token),
        )
        assert response.status_code == fa.status.HTTP_400_BAD_REQUEST

    async def test_add_like_to_own_post(self, async_client: AsyncClient, authed_user: AuthedUser):
        """Добавление лайка своему собственному посту."""
        post = PostsFactory.add(post_id=1, author_id=authed_user.id)
        response: Response = await async_client.post(
            url=self.get_url(post["id"]),
            headers=make_auth_header(authed_user.access_token),
        )
        assert response.status_code == fa.status.HTTP_400_BAD_REQUEST

    async def test_add_like_to_own_deleted_post(self, async_client: AsyncClient, authed_user: AuthedUser):
        """Добавление лайка своему собственному удаленному посту."""
        post = PostsFactory.add(post_id=1, author_id=authed_user.id, is_available=False)
        response: Response = await async_client.post(
            url=self.get_url(post["id"]),
            headers=make_auth_header(authed_user.access_token),
        )
        assert response.status_code == fa.status.HTTP_400_BAD_REQUEST

    async def test_add_like_to_other_post(self, async_client: AsyncClient, authed_user: AuthedUser):
        """Добавление лайка чужому посту."""
        another_user = UsersFactory.add(
            user_id=authed_user.id + 1,
            email="firstname2.secondname@domain.com",
        )
        post_id = 1
        PostsFactory.add(post_id=post_id, author_id=another_user["id"], likes=0)

        response: Response = await async_client.post(
            url=self.get_url(post_id),
            headers=make_auth_header(authed_user.access_token),
        )
        assert response.status_code == fa.status.HTTP_201_CREATED

        # Проверяем, что триггер сработал и счетчик изменился
        response: Response = await async_client.get(
            url=f"/posts/{post_id}",
            headers=make_auth_header(authed_user.access_token),
        )
        assert response.json()["likes"] == 1
