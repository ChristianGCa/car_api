# Release Notes (Notas de Lançamento) 🚀

Este documento registra o histórico de alterações, novas funcionalidades, correções de bugs e atualizações da **Car API**.

---

## [0.1.0] - 2026-07-06

Esta é a versão de lançamento inicial da **Car API**. O projeto foi estruturado para fornecer uma API estável de gerenciamento de frotas de carros e usuários.

### 🌟 Novas Funcionalidades
*   **Gestão de Usuários**: Cadastro de contas, listagem pública paginada e rotas protegidas de atualização/exclusão.
*   **Autenticação JWT**: Sistema seguro de login utilizando Bearer Token JWT e renovação automática via endpoint `/refresh`.
*   **Criptografia de Senhas**: Armazenamento seguro de senhas hash Argon2 via biblioteca `pwdlib`.
*   **Gestão de Marcas (CRUD)**: Mapeamento de fabricantes de automóveis com bloqueio de exclusão em caso de carros associados para assegurar a integridade.
*   **Gestão de Carros (CRUD)**: Controle individual de veículos por usuário.
    *   Filtros avançados de pesquisa: faixa de preço, combustível, transmissão, disponibilidade e termos de busca generalizados (modelo, placa ou cor).
    *   Validação rígida de campos (placa única, anos de fabricação e preço positivo).

### 🛡️ Segurança e Integridade
*   **Isolamento de Dados**: Usuários autenticados só conseguem listar ou manipular os carros criados por eles mesmos. Tentativas de acessar carros de terceiros retornam `403 Forbidden`.
*   **Banco de Dados Assíncrono**: Uso do driver assíncrono `aiosqlite` acoplado ao SQLAlchemy AsyncSession para garantir alta performance e concorrência sem bloqueios de I/O.
*   **Versionamento com Alembic**: Configuração de migrações automáticas para facilitar a rastreabilidade do banco de dados em equipe.

### 🛠️ Infraestrutura e Desenvolvimento
*   **Gerenciador Poetry**: Empacotamento de dependências unificado.
*   **Formatador Ruff**: Código padronizado de acordo com a PEP 8 e regras de formatação aplicadas em comandos curtos via `taskipy`.
*   **Suporte ao MkDocs**: Geração automática de site estático de documentação com tema `material` e suporte integrado para renderização de diagramas Mermaid.
