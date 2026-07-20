import pytest
from sqlalchemy import select

from car_api.models import User


@pytest.mark.asyncio  # Deve rodar de forma assíncrona
# Como marcamos a função session como fixture no outro arquivo,
# podemos passá-la como argumento
async def test_create_user(session):
    new_user = User(
        username='testuser', password='password', email='testuser@example.com'
    )
    session.add(new_user)
    await session.commit()

    user = await session.scalar(
        select(User).where(User.email == 'testuser@example.com')
    )

    new_user_data = {
        'id': user.id,
        'username': user.username,
        'password': user.password,
        'email': user.email,
    }

    assert new_user_data == {
        'id': 1,
        'username': 'testuser',
        'password': 'password',
        'email': 'testuser@example.com',
    }
