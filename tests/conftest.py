import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from car_api.app import app
from car_api.core.database import get_session
from car_api.core.security import create_access_token, get_password_hash
from car_api.models import Base
from car_api.models.cars import Brand, Car
from car_api.models.users import User


# Retorna uma sessão conectada e pronta no banco em memória para
# ser usada nos testes
@pytest_asyncio.fixture
async def session():
    engine = create_async_engine(url='sqlite+aiosqlite:///:memory:')

    async with engine.begin() as conn:
        # Cria as tabelas no banco de dados, pois Base
        # contém os modelos declarativos do SQLAlchemy
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSession(engine, expire_on_commit=False) as session:
        # Aqui, emprestamos a sessão para os testes
        yield session

    async with engine.begin() as conn:
        # Limpa as tabelas após os testes
        await conn.run_sync(Base.metadata.drop_all)


# O client abaixo irá substituir a dependência get_session do FastAPI
# para usar a sessão de teste
@pytest.fixture
def client(session):
    async def get_session_override():
        yield session  # Essa é a sessão do banco em memória

    with TestClient(app=app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def user_data():
    return {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password',
    }


@pytest_asyncio.fixture
# Isso serve para criar um usuário no banco, com
# os dados fornecidos por outras fixtures, e
# disponibilizá-lo para os testes
async def user(session, user_data):
    hashed_password = get_password_hash(user_data['password'])
    db_user = User(
        username=user_data['username'],
        email=user_data['email'],
        password=hashed_password,
    )
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user


@pytest.fixture
def token(user):
    return create_access_token(data={'sub': str(user.id)})


@pytest.fixture
def auth_headers(token):
    return {'Authorization': f'Bearer {token}'}


@pytest_asyncio.fixture
async def brand(session):
    db_brand = Brand(name='Toyota', description='Good cars')
    session.add(db_brand)
    await session.commit()
    await session.refresh(db_brand)
    return db_brand


@pytest_asyncio.fixture
async def car(session, brand, user):
    db_car = Car(
        model='Corolla',
        factory_year=2020,
        model_year=2021,
        color='Silver',
        plate='ABC1234',
        price=80000.0,
        fuel_type='gasoline',
        transmission='automatic',
        brand_id=brand.id,
        owner_id=user.id
    )
    session.add(db_car)
    await session.commit()
    await session.refresh(db_car)
    return db_car
