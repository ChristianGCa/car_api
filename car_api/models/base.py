from sqlalchemy.orm import DeclarativeBase


# Todas as tabelas do banco de dados herdarão dessa classe
class Base(DeclarativeBase):
    pass
