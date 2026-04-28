import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from backend.auth.utils import hash_password
from backend.models.user import User, UserRole


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient, db_session: AsyncSession):
    user = User(
        email="test@school.fr",
        hashed_password=hash_password("password123"),
        first_name="Jean",
        last_name="Dupont",
        role=UserRole.TEACHER,
    )
    db_session.add(user)
    await db_session.commit()

    response = await client.post(
        "/api/auth/token",
        data={"username": "test@school.fr", "password": "password123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["role"] == "teacher"


@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient):
    response = await client.post(
        "/api/auth/token",
        data={"username": "test@school.fr", "password": "mauvais"},
    )
    assert response.status_code == 401
