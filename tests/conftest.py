import pytest
import pytest_asyncio

from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from car_api.app import app
from car_api.core.database import get_session
from car_api.models import Base


# Retorna uma sessão conectada e pronta no banco em memória para
# ser usada nos testes
@pytest_asyncio.fixture
async def session():
    engine = create_async_engine(
        url="sqlite+aiosqlite:///:memory:"
    )

    async with engine.begin() as conn:
        # Cria as tabelas no banco de dados, pois Base
        # contém os modelos declarativos do SQLAlchemy
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSession(engine, expires_on_commit=False) as session:
        # Aqui, emprestamos a sessão para os testes
        yield session

    async with engine.begin() as conn:
        # Limpa as tabelas após os testes
        await conn.run_sync(Base.metadata.drop_all)


# O client abaixo irá substituir a dependência get_session do FastAPI
# para usar a sessão de teste
@pytest.fixture
def client(session):
    def get_session_override(_):
        return session  # Essa é a sessão do banco em memória

    with TestClient(app=app) as client:
        app.dependency_overrides[get_session] = get_session_override(session)
        yield client

    app.dependency_overrides.clear()
