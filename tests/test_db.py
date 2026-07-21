import pytest
from sqlalchemy import text


@pytest.mark.asyncio
async def test_db_connection(session):
    result = await session.execute(text("SELECT 1"))
    assert result.scalar() == 1


@pytest.mark.asyncio
async def test_db_consistency(session, user):
    result = await session.execute(
        text("SELECT username FROM users WHERE id = :id"), {"id": user.id}
    )
    assert result.scalar() == user.username
