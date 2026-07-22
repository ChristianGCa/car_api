# Car_api

## Para instalar

```bash
pipx install poetry
```

```bash
poetry python install 3.13
```

```bash
poetry env use 3.13
```

```bash
poetry install
```

Lembre de criar o .env:
```bash
DATABASE_URL=
JWT_SECRET_KEY=
JWT_ALGORITHM=
JWT_EXPIRATION_MINUTES=
```

## Para executar:
```bash
poetry run task run
```


Pacotes utilizados:

```bash
poetry add 'pydantic'
```

```bash
poetry add 'fastapi[standard]'
```

```bash
poetry add sqlalchemy[asyncio]
```

```bash
poetry add aiosqlite
```

```bash
poetry add pydantic-settings
```

```bash
poetry add alembic
```

```bash
poetry add "pwdlib[argon2]"
```

```bash
poetry add pyjwt
```
