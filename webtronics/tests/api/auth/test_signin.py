import fastapi as fa
from httpx import AsyncClient, Response
from tests.factories.users import UsersFactory
from utils.crypto import get_password_hash


class TestSignIn:
    @classmethod
    def get_url(cls) -> str:
        return "/auth/signin"

    async def test_wrong_creds(self, async_client: AsyncClient):
        """Поптыка входа с неправильными данными."""
        UsersFactory.add(1, "firstname.secondname@domain.com", get_password_hash("right-pass"))
        creds = {
            "email": "firstname.secondname@domain.com",
            "password": "wrong-pass",
        }
        response: Response = await async_client.post(url=self.get_url(), json=creds)
        assert response.status_code == fa.status.HTTP_400_BAD_REQUEST

    async def test_good_creds(self, async_client: AsyncClient):
        """Поптыка входа с правильными данными."""
        UsersFactory.add(1, "firstname.secondname@domain.com", get_password_hash("right-pass"))
        creds = {
            "email": "firstname.secondname@domain.com",
            "password": "right-pass",
        }
        response: Response = await async_client.post(url=self.get_url(), json=creds)
        assert response.status_code == fa.status.HTTP_200_OK
        assert "access_token" in response.json()
        assert "refresh_token" in response.json()
