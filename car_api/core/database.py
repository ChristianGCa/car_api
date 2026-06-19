from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from car_api.core.settings import Settings

# Criando o motor de conexão
engine = create_async_engine(Settings().DATABASE_URL)


async def get_session():
    async with AsyncSession(engine, expire_on_commit=False) as session:
        # yield serve para criar um gerador, que empresta a sessão para o
        # código que chama essa função, e depois fecha a sessão automaticamente
        yield session
