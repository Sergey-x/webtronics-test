import fastapi as fa
from httpx import AsyncClient, Response
from tests.conftest import AuthedUser
from tests.factories.posts import PostsFactory


class TestGetByIdPost:
    @classmethod
    def get_url(cls, post_id: int) -> str:
        return f"/posts/{post_id}"

    async def test_get_without_content(self, async_client: AsyncClient):
        """Получение поста с по несуществующему id."""
        response: Response = await async_client.get(
            url=self.get_url(1234),
        )
        assert response.status_code == fa.status.HTTP_404_NOT_FOUND

    async def test_get_without_content2(self, async_client: AsyncClient):
        """Получение поста с по несуществующему id."""
        response: Response = await async_client.get(
            url=self.get_url(-2),
        )
        assert response.status_code == fa.status.HTTP_404_NOT_FOUND

    async def test_get_without_auth_token(self, async_client: AsyncClient, authed_user: AuthedUser):
        """Получение поста без access токена."""
        post = PostsFactory.add(post_id=1, author_id=authed_user.id)
        response: Response = await async_client.get(
            url=self.get_url(post["id"]),
        )
        assert response.status_code == fa.status.HTTP_200_OK
