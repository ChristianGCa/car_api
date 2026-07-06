# Car API 🚗

Bem-vindo à documentação oficial da **Car API**, uma API REST robusta e completa para o gerenciamento de marcas e carros, desenvolvida com as melhores práticas de desenvolvimento em Python.

A API oferece recursos completos de CRUD (Create, Read, Update, Delete) para carros e marcas, controle de estoque/disponibilidade e um sistema de autenticação seguro baseado em JSON Web Tokens (JWT) com criptografia Argon2.

---

## 📌 Links de Navegação da Documentação

A documentação está dividida nas seguintes seções:

*   [**Instalação e Configuração** (installation_setup.md)](installation_setup.md): Instruções passo a passo de como preparar o ambiente, configurar variáveis de ambiente e rodar o projeto.
*   [**Estrutura do Projeto** (project_structure.md)](project_structure.md): Detalhamento da organização de diretórios e a responsabilidade de cada arquivo do projeto.
*   [**Endpoints da API** (api_endpoints.md)](api_endpoints.md): Lista completa de rotas, métodos HTTP, parâmetros e retornos esperados.
*   [**Modelagem do Sistema** (system_modeling.md)](system_modeling.md): Diagramas visuais (ERD, Arquitetura, Fluxos) desenhados com Mermaid.
*   [**Autenticação e Segurança** (auth_security.md)](auth_security.md): Explicações sobre o fluxo de geração e validação de tokens JWT, controle de acesso e segurança de dados.
*   [**Guidelines e Padrões** (guidelines_contribution.md)](guidelines_contribution.md): Convenções de código, uso de linters/formatadores e guia de contribuição no repositório.
*   [**Release Notes** (release_notes.md)](release_notes.md): Histórico de versões e alterações implementadas na API.

---

## 🛠️ Tecnologias Utilizadas

A stack principal de tecnologias do projeto inclui:

*   **FastAPI**: Framework web moderno, rápido (alta performance) e extremamente produtivo para construir APIs com Python.
*   **SQLAlchemy**: Toolkit SQL e mapeador objeto-relacional (ORM) robusto, configurado para operações assíncronas (`asyncio`).
*   **Alembic**: Ferramenta leve de migração de banco de dados para controle de versão do esquema do banco.
*   **SQLite (aiosqlite)**: Banco de dados relacional leve e embutido, acessado de forma assíncrona.
*   **Pydantic**: Biblioteca de validação de dados e gerenciamento de configurações usando type hints de Python.
*   **Argon2 (pwdlib)**: Algoritmo de hash de senhas de última geração e extremamente seguro para proteger as senhas dos usuários.
*   **PyJWT**: Implementação de JSON Web Token (JWT) para autenticação segura no fluxo Bearer Token.
*   **Poetry**: Ferramenta de gerenciamento de dependências e empacotamento em Python.
