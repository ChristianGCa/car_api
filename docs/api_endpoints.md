# Endpoints da API 🔗

Esta seção descreve todas as rotas da **Car API**, incluindo seus métodos HTTP, requisitos de autenticação, parâmetros esperados e os formatos de resposta.

---

## 📌 Links Rápidos do Servidor
*   **Swagger UI (Interativo)**: `/docs` (Ex: `http://127.0.0.1:8000/docs`)
*   **ReDoc (Detalhamento)**: `/redoc` (Ex: `http://127.0.0.1:8000/redoc`)

---

## 🔐 Autenticação (`/api/v1/auth`)

Endpoints voltados para a obtenção e renovação de tokens JWT.

### 1. Obter Token de Acesso
Gera um token JWT com base nas credenciais de e-mail e senha de um usuário existente.
*   **URL**: `/api/v1/auth/token`
*   **Método**: `POST`
*   **Autenticação**: Não requer (Público)
*   **Request Body (`LoginRequest`)**:
    ```json
    {
      "email": "usuario@exemplo.com",
      "password": "senha_segura"
    }
    ```
*   **Resposta de Sucesso (200 OK - `Token`)**:
    ```json
    {
      "access_token": "eyJhbGciOiJIUzI1NiIsIn...",
      "token_type": "bearer"
    }
    ```

### 2. Atualizar Token de Acesso (Refresh)
Gera um novo token JWT a partir de um token ainda válido enviado no cabeçalho.
*   **URL**: `/api/v1/auth/refresh`
*   **Método**: `POST`
*   **Autenticação**: Sim (Bearer Token no Header)
*   **Resposta de Sucesso (200 OK - `Token`)**:
    ```json
    {
      "access_token": "eyJhbGciOiJIUzI1NiIsIn...",
      "token_type": "bearer"
    }
    ```

---

## 👤 Usuários (`/api/v1/users`)

Gerenciamento de contas de usuário na plataforma.

### 1. Criar Usuário
Cadastra um novo usuário no banco de dados. A senha é criptografada automaticamente antes de salvar.
*   **URL**: `/api/v1/users/`
*   **Método**: `POST`
*   **Autenticação**: Não requer (Público)
*   **Request Body (`UserSchema`)**:
    ```json
    {
      "username": "joaodao",
      "email": "joao@exemplo.com",
      "password": "minhasenhasegura"
    }
    ```
*   **Resposta de Sucesso (201 Created - `UserPublicSchema`)**:
    ```json
    {
      "id": 1,
      "username": "joaodao",
      "email": "joao@exemplo.com",
      "created_at": "2026-07-06T13:00:00Z",
      "updated_at": "2026-07-06T13:00:00Z"
    }
    ```

### 2. Listar Usuários
Retorna uma lista paginada de todos os usuários do sistema.
*   **URL**: `/api/v1/users/`
*   **Método**: `GET`
*   **Autenticação**: Não requer (Público)
*   **Query Parameters**:
    *   `offset` (int, default=0): Registros para pular.
    *   `limit` (int, default=100, max=100): Limite de registros a retornar.
    *   `search` (string, opcional): Filtrar usuários pelo username ou email (case-insensitive).
*   **Resposta de Sucesso (200 OK - `UserListPublicSchema`)**:
    ```json
    {
      "users": [
        {
          "id": 1,
          "username": "joaodao",
          "email": "joao@exemplo.com",
          "created_at": "2026-07-06T13:00:00Z",
          "updated_at": "2026-07-06T13:00:00Z"
        }
      ],
      "offset": 0,
      "limit": 100
    }
    ```

### 3. Buscar Usuário por ID
Retorna os dados públicos de um usuário com base no ID dele.
*   **URL**: `/api/v1/users/{user_id}`
*   **Método**: `GET`
*   **Autenticação**: Não requer (Público)
*   **Resposta de Sucesso (200 OK - `UserPublicSchema`)**

### 4. Atualizar Usuário
Atualiza um ou mais campos de um usuário. Requer que quem esteja fazendo a requisição possua uma sessão válida.
*   **URL**: `/api/v1/users/{user_id}`
*   **Método**: `PUT`
*   **Autenticação**: Sim (Bearer Token)
*   **Request Body (`UserUpdateSchema`)**: Todos os campos são opcionais.
    ```json
    {
      "username": "novo_username",
      "email": "novo_email@exemplo.com",
      "password": "nova_senha_segura"
    }
    ```
*   **Resposta de Sucesso (201 Created - `UserPublicSchema`)**

### 5. Deletar Usuário
Remove um usuário do sistema.
*   **URL**: `/api/v1/users/{user_id}`
*   **Método**: `DELETE`
*   **Autenticação**: Sim (Bearer Token)
*   **Resposta de Sucesso**: `204 No Content`

---

## 🏷️ Marcas (`/api/v1/brands`)

Endpoints para cadastro e consulta de fabricantes de automóveis (Fiat, Chevrolet, etc.). **Todos estes endpoints exigem autenticação.**

### 1. Criar Marca
*   **URL**: `/api/v1/brands/`
*   **Método**: `POST`
*   **Autenticação**: Sim (Bearer Token)
*   **Request Body (`BrandSchema`)**:
    ```json
    {
      "name": "Ford",
      "description": "Fabricante americana de automóveis",
      "is_active": true
    }
    ```
*   **Resposta de Sucesso (201 Created - `BrandPublicSchema`)**

### 2. Listar Marcas
*   **URL**: `/api/v1/brands/`
*   **Método**: `GET`
*   **Autenticação**: Sim (Bearer Token)
*   **Query Parameters**:
    *   `offset` (int, default=0)
    *   `limit` (int, default=100)
    *   `search` (string, opcional): Filtrar marcas por nome.
    *   `is_active` (boolean, opcional): Filtrar marcas ativas (`true`) ou inativas (`false`).
*   **Resposta de Sucesso (200 OK - `BrandListPublicSchema`)**

### 3. Buscar Marca por ID
*   **URL**: `/api/v1/brands/{brand_id}`
*   **Método**: `GET`
*   **Autenticação**: Sim (Bearer Token)
*   **Resposta de Sucesso (200 OK - `BrandPublicSchema`)**

### 4. Atualizar Marca
*   **URL**: `/api/v1/brands/{brand_id}`
*   **Método**: `PUT`
*   **Autenticação**: Sim (Bearer Token)
*   **Request Body (`BrandUpdateSchema`)**
*   **Resposta de Sucesso (200 OK - `BrandPublicSchema`)**

### 5. Deletar Marca
Deleta uma marca cadastrada se, e somente se, não houver nenhum carro associado a ela.
*   **URL**: `/api/v1/brands/{brand_id}`
*   **Método**: `DELETE`
*   **Autenticação**: Sim (Bearer Token)
*   **Resposta de Sucesso**: `204 No Content`
*   **Erro (400 Bad Request)**: Retorna se a marca possuir carros associados.

---

## 🚗 Carros (`/api/v1/cars`)

Endpoints para controle do estoque de carros cadastrados. **Todos estes endpoints exigem autenticação.** Apenas carros pertencentes ao próprio usuário autenticado são exibidos ou alterados.

### 1. Criar Carro
*   **URL**: `/api/v1/cars/`
*   **Método**: `POST`
*   **Autenticação**: Sim (Bearer Token)
*   **Request Body (`CarSchema`)**:
    ```json
    {
      "model": "Uno Mille 1.0",
      "factory_year": 2013,
      "model_year": 2013,
      "color": "Prata",
      "plate": "ABC1C34",
      "fuel_type": "flex",
      "transmission": "manual",
      "price": 18500.00,
      "description": "Com escada no teto",
      "is_available": true,
      "brand_id": 1,
      "owner_id": 1
    }
    ```
*   **Resposta de Sucesso (201 Created - `CarPublicSchema`)**: Retorna o carro criado junto aos dados da marca e do proprietário completos.

### 2. Listar Carros
Retorna a lista de carros. **Esta rota filtra automaticamente os carros, retornando apenas os pertencentes ao usuário autenticado.**
*   **URL**: `/api/v1/cars/`
*   **Método**: `GET`
*   **Autenticação**: Sim (Bearer Token)
*   **Query Parameters (Filtros)**:
    *   `offset` / `limit` (Padrão: 0 / 100)
    *   `search` (string): Busca por modelo, cor ou placa.
    *   `brand_id` (int)
    *   `owner_id` (int)
    *   `fuel_type` (`gasoline` | `diesel` | `flex` | `ethanol` | `electric` | `hybrid`)
    *   `transmission` (`manual` | `automatic` | `semi_automatic` | `cvt`)
    *   `min_price` / `max_price` (float)
    *   `is_available` (boolean)
*   **Resposta de Sucesso (200 OK - `CarListPublicSchema`)**

### 3. Obter Detalhes de um Carro
Obtém informações detalhadas de um carro por ID. **Valida se o usuário autenticado é dono do carro solicitado.**
*   **URL**: `/api/v1/cars/{car_id}`
*   **Método**: `GET`
*   **Autenticação**: Sim (Bearer Token)
*   **Resposta de Sucesso (200 OK - `CarPublicSchema`)**
*   **Erro (403 Forbidden)**: Retorna se o carro pertencer a outro usuário.

### 4. Atualizar Carro
Atualiza um ou mais campos de um carro. **Valida se o usuário autenticado é dono do carro.**
*   **URL**: `/api/v1/cars/{car_id}`
*   **Método**: `PUT`
*   **Autenticação**: Sim (Bearer Token)
*   **Request Body (`CarUpdateSchema`)**: Todos os campos são opcionais.
*   **Resposta de Sucesso (200 OK - `CarPublicSchema`)**

### 5. Deletar Carro
Remove um carro do sistema. **Valida se o usuário autenticado é dono do carro.**
*   **URL**: `/api/v1/cars/{car_id}`
*   **Método**: `DELETE`
*   **Autenticação**: Sim (Bearer Token)
*   **Resposta de Sucesso**: `204 No Content`

---

## 💓 Health Check (`/health_check`)

Rota pública para verificação do status da aplicação.

*   **URL**: `/health_check`
*   **Método**: `GET`
*   **Autenticação**: Não requer (Público)
*   **Resposta de Sucesso (200 OK)**:
    ```json
    {
      "status": "ok"
    }
    ```
