# Instalação, Configuração e Deploy ⚙️

Este guia fornece instruções detalhadas sobre como preparar o seu ambiente local, configurar variáveis de ambiente, rodar o servidor de desenvolvimento, executar testes e fazer o deploy da aplicação.

---

## 📋 Pré-requisitos

Antes de iniciar, certifique-se de ter as seguintes ferramentas instaladas em sua máquina:

1.  **Python 3.13 ou superior**
2.  **Poetry**: Gerenciador de dependências e empacotamento. Caso não o tenha instalado, siga o [guia oficial de instalação do Poetry](https://python-poetry.org/docs/#installation).
3.  **Git**: Para clonar o repositório.

---

## 🚀 Instalação

Siga os passos abaixo para clonar o repositório e instalar as dependências do projeto:

1.  Clone o repositório em sua máquina local:
    ```bash
    git clone <url-do-repositorio>
    cd car_api
    ```

2.  Instale as dependências declaradas no arquivo [pyproject.toml](file:///home/chris/Documents/car_api/pyproject.toml):
    ```bash
    poetry install
    ```
    *Este comando criará um ambiente virtual isolado e instalará todas as dependências de produção e desenvolvimento.*

3.  Ative o ambiente virtual criado pelo Poetry (opcional, mas recomendado):
    ```bash
    poetry shell
    ```

---

## ⚙️ Configuração do Projeto

A aplicação utiliza o **Pydantic Settings** para carregar variáveis de ambiente a partir de um arquivo `.env` localizado na raiz do projeto.

1.  Crie um arquivo `.env` na raiz do projeto (copiando as variáveis exigidas):
    ```bash
    touch .env
    ```

2.  Preencha o arquivo `.env` com as seguintes variáveis de configuração:
    ```env
    DATABASE_URL=sqlite+aiosqlite:///./car_api.db
    JWT_SECRET_KEY=sua_chave_secreta_e_segura_aqui
    JWT_ALGORITHM=HS256
    JWT_EXPIRATION_MINUTES=30
    ```

    > [!IMPORTANT]
    > *   `DATABASE_URL`: Define o banco de dados. No exemplo acima, usamos SQLite de forma assíncrona (`sqlite+aiosqlite`).
    > *   `JWT_SECRET_KEY`: Uma chave secreta criptográfica forte. Nunca a exponha em repositórios públicos.
    > *   `JWT_EXPIRATION_MINUTES`: O tempo de expiração de cada token gerado (padrão de 30 minutos).

3.  Execute as migrações do banco de dados para criar as tabelas necessárias:
    ```bash
    poetry run alembic upgrade head
    ```

---

## 💻 Desenvolvimento

Com o ambiente instalado e configurado, você pode iniciar o servidor de desenvolvimento utilizando a tarefa automatizada no [pyproject.toml](file:///home/chris/Documents/car_api/pyproject.toml) gerenciada pela ferramenta `taskipy`:

```bash
poetry run task run
```

O comando acima iniciará o servidor FastAPI no modo de desenvolvimento (`fastapi dev car_api/app.py`). Por padrão, a aplicação estará acessível em:

*   **API**: [http://127.0.0.1:8000](http://127.0.0.1:8000)
*   **Swagger UI (Documentação Interativa)**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
*   **ReDoc (Documentação Alternativa)**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 🧪 Testes

Os testes da aplicação estão localizados no diretório [tests/](file:///home/chris/Documents/car_api/tests). Para criar e rodar a suíte de testes de forma limpa, você pode utilizar o `pytest`.

Como o `pytest` não vem instalado por padrão no grupo de dependências de desenvolvimento do projeto atual, você pode adicioná-lo executando:

```bash
poetry add --group dev pytest
```

E para executar a suíte de testes:

```bash
poetry run pytest
```

---

## 🚢 Deploy

Ao preparar a aplicação para produção (Deploy), siga as seguintes recomendações:

### 1. Banco de Dados de Produção
Para ambientes de produção, substitua o SQLite por um banco de dados relacional robusto (ex: PostgreSQL) alterando a variável `DATABASE_URL` no `.env` de produção:
```env
DATABASE_URL=postgresql+asyncpg://usuario:senha@host:porta/nome_banco
```
*(Nota: Certifique-se de instalar o driver adequado, como `asyncpg`, se mudar para o PostgreSQL).*

### 2. Executando Migrações em Produção
Antes de iniciar a aplicação no servidor de produção, garanta que o banco de dados esteja na versão mais recente executando:
```bash
alembic upgrade head
```

### 3. Servidor ASGI de Produção
Em produção, não use `fastapi dev`. Execute a aplicação com um servidor ASGI de alta performance como o `uvicorn` diretamente ou gerenciado pelo `gunicorn`:
```bash
poetry run uvicorn car_api.app:app --host 0.0.0.0 --port 8000 --workers 4
```
*(Ajuste o número de workers com base nos recursos de CPU do seu servidor).*
