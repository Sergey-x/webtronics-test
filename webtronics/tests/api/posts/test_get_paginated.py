import fastapi as fa
from httpx import AsyncClient, Response


class TestGetPaginatedPosts:
    @classmethod
    def get_url(cls) -> str:
        return "/posts"

    async def test_get_many_without_params(self, async_client: AsyncClient):
        """Получение постов."""
        response: Response = await async_client.get(url=self.get_url())
        assert response.status_code == fa.status.HTTP_200_OK

    async def test_check_default_paginate_fields(self, async_client: AsyncClient):
        """Получение постов."""
        response: Response = await async_client.get(url=self.get_url())
        response_body = response.json()
        assert "total" in response_body
        assert response_body["page"] == 1
        assert response_body["size"] == 50
        assert "pages" in response_body
