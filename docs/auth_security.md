# Autenticação e Segurança 🔒

A segurança é um dos pilares da **Car API**. O projeto implementa criptografia moderna de senhas e autenticação sem estado (stateless) via JSON Web Tokens (JWT).

---

## 🔑 Criptografia de Senhas

As senhas dos usuários nunca são armazenadas em texto plano no banco de dados.
*   **Algoritmo**: O hash é gerado utilizando o algoritmo **Argon2**, recomendado pela biblioteca `pwdlib` (`pwdlib[argon2]`), através da classe `PasswordHash.recommended()`.
*   **Função**:
    *   `get_password_hash(password: str)`: Utiliza o contexto criptográfico para gerar o hash seguro de forma unidirecional.
    *   `verify_password(plain_password: str, hashed_password: str)`: Compara a senha informada no login com o hash armazenado de forma segura contra ataques de tempo.

---

## 🎟️ Autenticação baseada em JWT

A autenticação é efetuada através do fluxo **OAuth2 Bearer Token**:

1.  **Geração do Token**:
    *   O endpoint `/api/v1/auth/token` recebe as credenciais.
    *   Caso válidas, o servidor cria um payload JWT contendo o ID do usuário como o assunto (`sub`).
    *   O token é assinado com o algoritmo **HS256** utilizando a chave secreta carregada em `settings.JWT_SECRET_KEY`.
    *   O token expira após o tempo configurado em `settings.JWT_EXPIRATION_MINUTES` (padrão de 30 minutos).

2.  **Payload do Token (Claims)**:
    *   `sub` (Subject): ID do usuário convertido para string.
    *   `exp` (Expiration): Timestamp UNIX correspondente à data/hora de expiração do token.

3.  **Validação**:
    *   A função `verify_token(token)` decodifica e analisa o token recebido.
    *   Caso o token esteja expirado, lança `HTTP 401 Unauthorized` com a mensagem `"Token has expired"`.
    *   Caso seja inválido ou corrompido, lança `HTTP 401 Unauthorized` com a mensagem `"Could not validate credentials"`.

---

## 🛡️ Controle de Acesso e Regras de Negócio

### 1. Injeção de Dependência (`Depends`)
As rotas protegidas utilizam a dependência `get_current_user` injetada através do FastAPI. Esta dependência realiza as seguintes ações:
*   Extrai as credenciais enviadas no cabeçalho `Authorization: Bearer <TOKEN>`.
*   Chama `verify_token` para decodificar e atestar a validade do token.
*   Recupera o usuário do banco de dados SQLite correspondente ao ID informado no campo `sub`.
*   Lança `HTTP 401 Unauthorized` caso o usuário não seja localizado no banco.
*   Caso tudo ocorra com sucesso, injeta o objeto de dados `User` no manipulador da rota.

### 2. Visibilidade Restrita de Recursos (Dono do Carro)
O gerenciador de carros no banco de dados aplica filtros rígidos com base no usuário logado para mitigar brechas de segurança:
*   **Listagem (`GET /api/v1/cars/`)**:
    *   Filtra os carros por `Car.owner_id == current_user.id` no banco de dados. Um usuário logado **não consegue ver** carros cadastrados por outros usuários, mesmo fornecendo filtros adicionais.
*   **Acesso Direto, Atualização e Exclusão (`GET/PUT/DELETE /api/v1/cars/{car_id}`)**:
    *   O sistema busca o carro no banco pelo ID e chama a função `verify_car_ownership(user, car.owner_id)`.
    *   Se `user.id != car.owner_id`, é disparada imediatamente uma exceção `HTTP 403 Forbidden` com a mensagem: `"You do not have permission to access this car"`.

### 3. Exclusão de Marcas Associadas
Para garantir a integridade referencial e segurança do sistema, não é permitida a exclusão de marcas (`DELETE /api/v1/brands/{brand_id}`) caso existam carros cadastrados com essa chave estrangeira. Uma tentativa resulta em `HTTP 400 Bad Request`.
