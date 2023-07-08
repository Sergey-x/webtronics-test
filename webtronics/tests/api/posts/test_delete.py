import datetime

import fastapi as fa
from httpx import AsyncClient, Response
from tests.conftest import AuthedUser, make_auth_header
from tests.factories.posts import PostsFactory


class TestCreatePost:
    @classmethod
    def get_url(cls, post_id: int) -> str:
        return f"/posts/{post_id}"

    async def test_delete_by_wrong_id(self, async_client: AsyncClient, authed_user: AuthedUser):
        """Удаление поста с несуществующим id."""
        response: Response = await async_client.delete(url=self.get_url(1234),
                                                       headers=make_auth_header(authed_user.access_token))
        assert response.status_code == fa.status.HTTP_404_NOT_FOUND

    async def test_good_create(self, async_client: AsyncClient, authed_user: AuthedUser):
        """Успешное удаление поста."""
        user_id: int = authed_user.id
        post = PostsFactory.add(post_id=1, author_id=user_id, dt_created=datetime.datetime.now())

        response: Response = await async_client.delete(
            url=self.get_url(post["id"]),
            headers=make_auth_header(authed_user.access_token),
        )
        assert response.status_code == fa.status.HTTP_204_NO_CONTENT

        response: Response = await async_client.delete(
            url=self.get_url(post["id"]),
            headers=make_auth_header(authed_user.access_token),
        )
        assert response.status_code == fa.status.HTTP_204_NO_CONTENT

    async def test_delete_without_auth_token(self, async_client: AsyncClient, authed_user: AuthedUser):
        """Удаление поста без токена доступа."""
        post = PostsFactory.add(post_id=1, author_id=authed_user.id, dt_created=datetime.datetime.now())
        response: Response = await async_client.delete(url=self.get_url(post["id"]))
        assert response.status_code == fa.status.HTTP_401_UNAUTHORIZED
