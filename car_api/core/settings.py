from pydantic_settings import BaseSettings, SettingsConfigDict


# Essa classe carrega as variáveis de ambiente e torna acessível por meio de atributos
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
    )

    DATABASE_URL: str

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = 'HS256'
    JWT_EXPIRATION_MINUTES: int = 30

