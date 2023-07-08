import fastapi as fa
from fastapi_jwt_auth import AuthJWT
from httpx import AsyncClient, Response
from tests.conftest import make_auth_header


class TestSignIn:
    TEST_SUBJECT: int = 1

    @classmethod
    def get_url(cls) -> str:
        return "/auth/refresh"

    async def test_refresh_with_access_token(self, async_client: AsyncClient):
        """Обновление пары JWT с помощью access токена."""
        access_token: str = AuthJWT().create_access_token(subject=self.TEST_SUBJECT)

        response: Response = await async_client.post(url=self.get_url(), headers=make_auth_header(token=access_token))
        assert response.status_code == fa.status.HTTP_401_UNAUTHORIZED

    async def test_good_refresh(self, async_client: AsyncClient):
        """Обновление пары JWT с помощью refresh токена."""
        refresh_token: str = AuthJWT().create_refresh_token(subject=self.TEST_SUBJECT)

        response: Response = await async_client.post(url=self.get_url(), headers=make_auth_header(token=refresh_token))
        assert response.status_code == fa.status.HTTP_200_OK
        assert "access_token" in response.json()
        assert "refresh_token" in response.json()
