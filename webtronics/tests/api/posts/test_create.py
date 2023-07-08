import fastapi as fa
from httpx import AsyncClient, Response
from tests.conftest import AuthedUser, make_auth_header


class TestCreatePost:
    @classmethod
    def get_url(cls) -> str:
        return "/posts"

    @classmethod
    def get_good_post_data(cls) -> dict:
        return {
            "text": "some content",
        }

    async def test_create_without_content(self, async_client: AsyncClient, authed_user: AuthedUser):
        """Создание поста с некорректными данными или без них."""
        response: Response = await async_client.post(
            url=self.get_url(),
            headers=make_auth_header(authed_user.access_token),
        )
        assert response.status_code == fa.status.HTTP_400_BAD_REQUEST

    async def test_create_without_auth_token(self, async_client: AsyncClient):
        """Создание поста без токена доступа."""
        response: Response = await async_client.post(url=self.get_url(), json=self.get_good_post_data())
        assert response.status_code == fa.status.HTTP_401_UNAUTHORIZED

    async def test_good_create(self, async_client: AsyncClient, authed_user: AuthedUser):
        """Успешное создание поста."""
        response: Response = await async_client.post(
            url=self.get_url(),
            json=self.get_good_post_data(),
            headers=make_auth_header(authed_user.access_token),
        )
        assert response.status_code == fa.status.HTTP_201_CREATED
        created_post: dict = response.json()

        # проверяем корректность установленных полей
        assert created_post["text"] == "some content"
        assert created_post["author_id"] == authed_user.id
        assert created_post["is_available"]
        assert created_post["dt_updated"] is None
        assert created_post["dt_created"] is not None
        assert created_post["likes"] == 0
