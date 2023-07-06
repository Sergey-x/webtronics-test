import fastapi as fa
from httpx import AsyncClient, Response


class TestSignUp:
    @classmethod
    def get_url(cls) -> str:
        return "/auth/signup"

    async def test_too_short_password(self, async_client: AsyncClient):
        """Регистрация с коротким паролем."""
        creds = {
            "email": "firstname.secondname@domain.com",
            "password": "1234",
        }
        response: Response = await async_client.post(url=self.get_url(), json=creds)
        assert response.status_code == fa.status.HTTP_400_BAD_REQUEST

    async def test_without_email(self, async_client: AsyncClient):
        """Регистрация без email."""
        creds = {
            "password": "123456",
        }
        response: Response = await async_client.post(url=self.get_url(), json=creds)
        assert response.status_code == fa.status.HTTP_400_BAD_REQUEST

    async def test_without_password(self, async_client: AsyncClient):
        """Регистрация без пароля."""
        creds = {
            "email": "firstname.secondname@domain.com",
        }
        response: Response = await async_client.post(url=self.get_url(), json=creds)
        assert response.status_code == fa.status.HTTP_400_BAD_REQUEST

    async def test_without_any_data(self, async_client: AsyncClient):
        """Регистрация без данных."""
        response: Response = await async_client.post(url=self.get_url())
        assert response.status_code == fa.status.HTTP_400_BAD_REQUEST

    async def test_duplicated_email(self, async_client: AsyncClient):
        """Регистрация с email-ом, который уже зарегистрирован в системе."""
        pass

    async def test_good_signup(self, async_client: AsyncClient):
        """Успешная регистрация."""
        creds = {
            "email": "firstname.secondname@domain.com",
            "password": "123456",
        }
        response: Response = await async_client.post(url=self.get_url(), json=creds)
        assert response.status_code == fa.status.HTTP_201_CREATED

    async def test_good_with_good_jwt(self, async_client: AsyncClient):
        creds = {
            "email": "firstname.secondname@domain.com",
            "password": "123456",
        }
        response: Response = await async_client.post(url=self.get_url(), json=creds, headers={"Authorization": ""})
        assert response.status_code == fa.status.HTTP_201_CREATED

    async def test_good_with_bad_jwt(self, async_client: AsyncClient):
        pass
