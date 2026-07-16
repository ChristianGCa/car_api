import pytest_asyncio

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from car_api.models import Base


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