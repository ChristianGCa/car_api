# Estrutura do Projeto 📂

Abaixo está detalhada a organização de diretórios e arquivos do repositório da **Car API**, explicando a responsabilidade de cada pasta e módulo.

---

## 🌳 Árvore de Diretórios

A estrutura geral do projeto está organizada da seguinte forma:

```text
car_api/
├── alembic.ini              # Arquivo de configuração das migrações do Alembic
├── car_api/                 # Código-fonte principal da aplicação
│   ├── __init__.py
│   ├── app.py               # Ponto de entrada (criação do app FastAPI e registro de rotas)
│   ├── core/                # Módulos globais e configurações de base
│   │   ├── database.py      # Conexão assíncrona do SQLAlchemy e gerador de sessão
│   │   ├── security.py      # Autenticação, senhas e validação de tokens JWT
│   │   └── settings.py      # Definição e carregamento de configurações do .env
│   ├── models/              # Modelos de dados do banco (Entidades do SQLAlchemy)
│   │   ├── __init__.py
│   │   ├── base.py          # Classe base declarativa do SQLAlchemy
│   │   ├── cars.py          # Modelos de Carro (Car) e Marca (Brand)
│   │   └── users.py         # Modelo de Usuário (User)
│   ├── routers/             # Definição das rotas HTTP (Controladores)
│   │   ├── auth.py          # Endpoints de login e refresh token
│   │   ├── brands.py        # Endpoints para gerenciamento de marcas
│   │   ├── cars.py          # Endpoints para gerenciamento de carros
│   │   └── users.py         # Endpoints para gerenciamento de usuários
│   └── schemas/             # Esquemas de validação de dados (Pydantic Models)
│       ├── auth.py          # Schemas de request e response de autenticação
│       ├── brands.py        # Schemas para criação, atualização e listagem de marcas
│       ├── cars.py          # Schemas para criação, atualização e listagem de carros
│       └── users.py         # Schemas para criação, atualização e listagem de usuários
├── docs/                    # Pasta que contém esta documentação do projeto (.md)
├── migrations/              # Arquivos de migração gerados pelo Alembic
│   ├── env.py               # Script de configuração do ambiente de migração
│   ├── script.py.mako       # Template para geração de novas migrações
│   └── versions/            # Scripts de histórico de alterações de banco de dados
├── mkdocs.yml               # Arquivo de configuração de geração da página MkDocs
├── poetry.lock              # Arquivo de bloqueio de versões exatas das dependências
├── pyproject.toml           # Arquivo de configuração do Poetry, dependências e tarefas do Ruff/Taskipy
├── README.md                # Visão rápida do repositório
└── tests/                   # Testes automatizados do sistema
    └── __init__.py
```

---

## 🧩 Detalhamento das Camadas do Código

### 1. `app.py`
O arquivo [app.py](file:///home/chris/Documents/car_api/car_api/app.py) é o cérebro da inicialização da API. Ele instancia a classe principal `FastAPI`, inclui os roteadores definindo seus respectivos prefixos (como `/api/v1/auth`, `/api/v1/users`, etc.) e define o endpoint global `/health_check` que indica a saúde do servidor.

### 2. Camada Core (`core/`)
Contém as utilidades cruciais que servem de alicerce para toda a aplicação:
*   [settings.py](file:///home/chris/Documents/car_api/car_api/core/settings.py): Centraliza as propriedades de configuração carregadas do `.env` como as credenciais do banco e chaves do JWT.
*   [database.py](file:///home/chris/Documents/car_api/car_api/core/database.py): Cria o motor assíncrono (`AsyncEngine`) a partir da URL fornecida e exporta a dependência `get_session()` que gerencia o ciclo de vida de cada conexão (`AsyncSession`).
*   [security.py](file:///home/chris/Documents/car_api/car_api/core/security.py): Contém os utilitários de criptografia (hashing com Argon2 e tokens com JWT), autenticação de usuários, extração do usuário logado através do cabeçalho HTTP Bearer e validação de posse de recursos.

### 3. Modelos de Banco de Dados (`models/`)
Utilizam o mapeamento declarativo moderno do SQLAlchemy 2.0 (`Mapped` e `mapped_column`):
*   [base.py](file:///home/chris/Documents/car_api/car_api/models/base.py): Contém a classe `Base` herdada de `DeclarativeBase`.
*   [users.py](file:///home/chris/Documents/car_api/car_api/models/users.py): Define o modelo `User`, contendo ID, username, e-mail, senha criptografada e datas de controle. Contém o relacionamento um-para-muitos com carros.
*   [cars.py](file:///home/chris/Documents/car_api/car_api/models/cars.py): Define o modelo `Car`, os Enums `Transmission` e `FuelType`, e o modelo `Brand`. Inclui chaves estrangeiras que ligam carros a marcas e a usuários (donos).

### 4. Roteadores (`routers/`)
Implementam a lógica de endpoints e as regras de negócio de fluxo HTTP:
*   [auth.py](file:///home/chris/Documents/car_api/car_api/routers/auth.py): Lida com a emissão do token e o fluxo de renovação.
*   [users.py](file:///home/chris/Documents/car_api/car_api/routers/users.py): Implementa criação, busca, listagem, atualização e deleção de usuários.
*   [brands.py](file:///home/chris/Documents/car_api/car_api/routers/brands.py): Controla o gerenciamento de marcas de carros.
*   [cars.py](file:///home/chris/Documents/car_api/car_api/routers/cars.py): Gerencia os carros cadastrados no sistema, aplicando as restrições de visibilidade e alteração com base no dono logado.

### 5. Camada de Schemas (`schemas/`)
Define os modelos de validação do Pydantic para entrada e saída de dados. Eles asseguram que os dados enviados pelos clientes estão corretos e formatam os dados enviados pelo servidor (ocultando campos sensíveis como senhas e carregando objetos aninhados, como informações da marca ou do dono do carro).
