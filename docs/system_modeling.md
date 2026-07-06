# Modelagem do Sistema 📊

Esta página apresenta os modelos visuais da **Car API** mapeando as entidades, a estrutura arquitetural e os principais fluxos de processamento do sistema.

---

## 🗄️ Modelos de Dados (ERD)

O diagrama abaixo ilustra as tabelas do banco de dados (geradas pelas classes SQLAlchemy em [models](file:///home/chris/Documents/car_api/car_api/models)), suas colunas, chaves primárias/estrangeiras e os relacionamentos.

```mermaid
erDiagram
    users ||--o{ cars : "possui (1:N)"
    brands ||--o{ cars : "contém (1:N)"

    users {
        int id PK
        string username "unique"
        string password "argon2 hash"
        string email "unique"
        datetime created_at
        datetime updated_at
    }

    brands {
        int id PK
        string name "unique, max 50"
        boolean is_active "default true"
        string description "text, nullable"
        datetime created_at
        datetime updated_at
    }

    cars {
        int id PK
        string model "max 100"
        int factory_year
        int model_year
        string color "max 30"
        string plate "unique, indexed, max 10"
        string fuel_type "enum (gasoline/diesel/flex/ethanol/electric/hybrid)"
        string transmission "enum (manual/automatic/semi_automatic/cvt)"
        decimal price "Numeric(10,2)"
        string description "text, nullable"
        boolean is_available "default true"
        int brand_id FK
        int owner_id FK
        datetime created_at
        datetime updated_at
    }
```

---

## 🏛️ Arquitetura do Sistema

A API segue uma arquitetura em camadas estruturada em torno do ecossistema FastAPI e SQLAlchemy, mapeada a seguir:

```mermaid
graph TD
    Client[Cliente HTTP<br/>Web, Mobile, Postman] <--> API[FastAPI Application<br/>car_api/app.py]
    
    subgraph FastAPI Core
        API <--> Routers[Routers<br/>auth, users, brands, cars]
        Routers <--> Security[Segurança e Dependências<br/>core/security.py]
        Routers <--> Schemas[Validação de Schemas<br/>schemas/]
    end

    subgraph Database Access Layer
        Routers <--> SQLAlchemy[SQLAlchemy ORM<br/>core/database.py & models/]
    end

    SQLAlchemy <--> SQLite[(SQLite Database<br/>aiosqlite)]
```

---

## 🔐 Fluxo de Autenticação

Fluxo de requisição para obter o token de acesso (login) e renová-lo (refresh) usando JWT.

```mermaid
sequenceDiagram
    autonumber
    actor Cliente
    participant Auth as Router de Autenticação
    participant Security as Segurança (core/security)
    participant DB as Banco de Dados (SQLite)

    Cliente->>Auth: POST /api/v1/auth/token (LoginRequest)
    Auth->>Security: authenticate_user(email, password)
    Security->>DB: Buscar User por e-mail
    DB-->>Security: Retorna User ou None
    Security->>Security: verificar senha (verify_password com Argon2)
    Security-->>Auth: Retorna User se válido
    
    alt Credenciais Inválidas
        Auth-->>Cliente: HTTP 401 Unauthorized
    else Credenciais Válidas
        Auth->>Security: create_access_token(sub=user_id)
        Security-->>Auth: Retorna string JWT
        Auth-->>Cliente: HTTP 200 OK (access_token, token_type='bearer')
    end
```

---

## 🚗 Fluxo CRUD de Carros (Autorização)

Abaixo está exemplificado o fluxo de leitura detalhada de um carro (`GET /cars/{id}`), ilustrando a validação de permissões realizada para certificar que o usuário solicitante é o dono do recurso.

```mermaid
sequenceDiagram
    autonumber
    actor Cliente
    participant Router as Router de Carros
    participant Dep as get_current_user (Dependency)
    participant DB as Banco de Dados (SQLite)
    
    Cliente->>Router: GET /api/v1/cars/{car_id} (Header Authorization: Bearer JWT)
    Router->>Dep: get_current_user(token)
    Dep-->>Router: Retorna User autenticado
    Router->>DB: Buscar Car por car_id (com selectinload)
    DB-->>Router: Retorna Car ou None
    
    alt Carro Não Existe
        Router-->>Cliente: HTTP 404 Not Found
    else Carro Existe
        Router->>Router: verify_car_ownership(user, car.owner_id)
        alt Usuário não é o dono (user.id != car.owner_id)
            Router-->>Cliente: HTTP 403 Forbidden
        else Usuário é o dono
            Router-->>Cliente: HTTP 200 OK (Detalhes do Carro)
        end
    end
```

---

## 🛡️ Fluxo de Segurança (Validação de Token)

Este diagrama representa a esteira de validação efetuada em todas as rotas protegidas pelo sistema antes de liberar o processamento da rota final.

```mermaid
graph TD
    Request[Requisição do Cliente com Token Bearer] --> AuthHeader{Possui Header<br/>Authorization?}
    AuthHeader -- Não --> HTTP401[HTTP 401 Unauthorized<br/>HTTPBearer required]
    AuthHeader -- Sim --> DecodeJWT{Decodificar JWT<br/>verify_token}
    DecodeJWT -- ExpiredSignatureError --> HTTP401_Exp[HTTP 401 Unauthorized<br/>Token has expired]
    DecodeJWT -- InvalidTokenError --> HTTP401_Inv[HTTP 401 Unauthorized<br/>Could not validate credentials]
    DecodeJWT -- Sucesso --> ExtractSub{Possui 'sub'<br/>no payload?}
    ExtractSub -- Não --> HTTP401_Inv
    ExtractSub -- Sim --> DBCheck{Buscar User<br/>no Banco}
    DBCheck -- Não encontrado --> HTTP401_User[HTTP 401 Unauthorized<br/>User not found]
    DBCheck -- Encontrado --> CheckRoute{Rota requer<br/>verificação de posse?}
    CheckRoute -- Não --> ExecRoute[Executa Rota]
    CheckRoute -- Sim --> OwnershipCheck{ID do Dono ==<br/>ID do Usuário?}
    OwnershipCheck -- Não --> HTTP403[HTTP 403 Forbidden<br/>You do not have permission]
    OwnershipCheck -- Sim --> ExecRoute
```
