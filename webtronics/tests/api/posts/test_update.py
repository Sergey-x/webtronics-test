import fastapi as fa
from httpx import AsyncClient, Response
from tests.conftest import AuthedUser, make_auth_header
from tests.factories.posts import PostsFactory
from tests.factories.users import UsersFactory
from utils.crypto import get_password_hash


class TestCreatePost:
    @classmethod
    def get_url(cls, post_id: int) -> str:
        return f"/posts/{post_id}"

    @classmethod
    def get_good_post_data(cls) -> dict:
        return {
            "text": "new content",
        }

    async def test_update_without_content(self, async_client: AsyncClient, authed_user: AuthedUser):
        """Обновление поста с некорректными данными или без них."""
        user_id: int = authed_user.id
        post = PostsFactory.add(post_id=1, author_id=user_id)
        response: Response = await async_client.patch(
            url=self.get_url(post["id"]),
            headers=make_auth_header(authed_user.access_token),
        )
        assert response.status_code == fa.status.HTTP_400_BAD_REQUEST

    async def test_update_without_auth_token(self, async_client: AsyncClient):
        """Обновление поста без токена доступа."""
        response: Response = await async_client.patch(url=self.get_url(1), json=self.get_good_post_data())
        assert response.status_code == fa.status.HTTP_401_UNAUTHORIZED

    async def test_good_update(self, async_client: AsyncClient, authed_user: AuthedUser):
        """Успешное обновление поста."""
        post = PostsFactory.add(post_id=1, author_id=authed_user.id)

        response: Response = await async_client.patch(
            url=self.get_url(post["id"]),
            json=self.get_good_post_data(),
            headers=make_auth_header(authed_user.access_token),
        )
        assert response.status_code == fa.status.HTTP_200_OK
        updated_post: dict = response.json()

        # проверяем корректность установленных полей
        assert updated_post["text"] == self.get_good_post_data()["text"]
        assert updated_post["author_id"] == authed_user.id
        assert updated_post["is_available"]
        assert updated_post["dt_updated"] is not None
        assert updated_post["dt_created"] is not None
        assert updated_post["likes"] == 0

    async def test_update_other_user_post(self, async_client: AsyncClient, authed_user: AuthedUser):
        """Обновление чужого поста."""
        other_user = UsersFactory.add(2, "firstname2.secondname@domain.com", get_password_hash("right-pass"))
        post = PostsFactory.add(post_id=1, author_id=other_user["id"])

        response: Response = await async_client.patch(url=self.get_url(post["id"]),
                                                      json=self.get_good_post_data(),
                                                      headers=make_auth_header(authed_user.access_token))
        assert response.status_code == fa.status.HTTP_404_NOT_FOUND

    async def test_update_deleted_post(self, async_client: AsyncClient, authed_user: AuthedUser):
        """Обновление удаленного поста."""
        deleted_post = PostsFactory.add(post_id=1, author_id=authed_user.id, is_available=False)

        response: Response = await async_client.patch(url=self.get_url(deleted_post["id"]),
                                                      json=self.get_good_post_data(),
                                                      headers=make_auth_header(authed_user.access_token))
        assert response.status_code == fa.status.HTTP_404_NOT_FOUND
