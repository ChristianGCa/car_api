# Guidelines e Contribuição 🤝

Para manter a base de código limpa, legível e de fácil manutenção por múltiplos desenvolvedores, a **Car API** segue padrões estritos de qualidade de código. Siga as diretrizes abaixo ao contribuir para o repositório.

---

## 🎨 Guidelines e Padrões de Código

### 1. Padrões Gerais
*   **Python**: Compatibilidade mínima com a versão **Python 3.13**.
*   **PEP 8**: A base de código respeita as diretrizes oficiais de estilo do Python.
*   **Operações Assíncronas (`async/await`)**: Todas as chamadas ao banco de dados e rotas HTTP devem ser escritas de forma assíncrona usando `AsyncSession` do SQLAlchemy e o driver `aiosqlite`.
*   **Preservação de Documentação**: Mantenha sempre os comentários e docstrings explicativos e atualizados ao modificar qualquer função.

### 2. Validação e Schemas
*   Todas as entradas de endpoints devem ser validadas por classes Pydantic (`BaseModel`).
*   Regras complexas de validação (como tamanho mínimo de string, formato de placa ou valores numéricos maiores que zero) devem ser implementadas usando `@field_validator` diretamente nos schemas do Pydantic.
*   Os retornos da API devem ocultar dados confidenciais (por exemplo, a senha de usuários) utilizando Schemas públicos dedicados (ex: `UserPublicSchema`).

### 3. Ferramentas Automáticas de Estilo (Ruff)
O projeto utiliza o **Ruff** como o linter e formatador oficial de código. As configurações estão descritas na seção `[tool.ruff]` do arquivo [pyproject.toml](file:///home/chris/Documents/car_api/pyproject.toml):
*   **Comprimento de Linha**: Máximo de 79 caracteres.
*   **Aspas**: Preferência por aspas simples (`'`).
*   **Imports**: Organizados automaticamente pelo Ruff.

As tarefas estão automatizadas via `taskipy`:
*   Para verificar se há problemas de estilo (linter):
    ```bash
    poetry run task lint
    ```
*   Para formatar o código automaticamente e corrigir erros comuns:
    ```bash
    poetry run task format
    ```

---

## 💻 Processo de Contribuição

Para enviar alterações para o projeto, siga o fluxo de trabalho abaixo:

### Passo 1: Preparar o Trabalho
1.  Faça um Fork do repositório original (se aplicável) ou clone-o diretamente.
2.  Crie uma nova ramificação (branch) de feature partindo da branch principal:
    ```bash
    git checkout -b feature/nome-da-sua-feature
    ```

### Passo 2: Codificação e Padrões
1.  Implemente a funcionalidade ou correção.
2.  Garanta que a formatação e as regras do linter passem sem erros:
    ```bash
    poetry run task format
    ```
3.  Crie os testes correspondentes no diretório [tests/](file:///home/chris/Documents/car_api/tests).

### Passo 3: Testar e Documentar
1.  Rode os testes locais para garantir que nenhuma regressão foi introduzida:
    ```bash
    poetry run pytest
    ```
2.  Caso tenha alterado tabelas ou campos do banco de dados, crie uma nova migração utilizando o Alembic:
    ```bash
    poetry run alembic revision --autogenerate -m "descricao da alteracao"
    ```
3.  Atualize a documentação da API em `/docs` se novos endpoints ou atributos forem inseridos.

### Passo 4: Envio
1.  Faça o commit de suas alterações com uma mensagem descritiva:
    ```bash
    git commit -m "feat: adiciona endpoint de busca de carro por placa"
    ```
2.  Envie o branch para o repositório remoto:
    ```bash
    git push origin feature/nome-da-sua-feature
    ```
3.  Abra um **Pull Request (PR)** explicando detalhadamente o que foi feito, as justificativas de design e como a funcionalidade foi testada.
