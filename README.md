# Finance.py - Gerenciador Financeiro Pessoal

Uma aplicação de desktop desenvolvida em Python com Tkinter para o gerenciamento de finanças pessoais. O projeto permite que os usuários controlem suas receitas, despesas e investimentos de forma visual e intuitiva, com um dashboard interativo.

## ✨ Funcionalidades

- **Autenticação de Usuário**: Sistema seguro de Login e Cadastro.
- **Criptografia de Senhas**: As senhas dos usuários são criptografadas antes de serem salvas no banco de dados.
- **Validação de CPF**: Garante que o CPF inserido no cadastro seja válido.
- **Dashboard Interativo**:
  - Resumo financeiro com Saldo, Receitas, Despesas e Investimentos.
  - Gráfico de pizza para visualização do fluxo financeiro mensal.
  - Barras de progresso para análise de gastos e investimentos por categoria.
- **Gerenciamento de Transações (CRUD)**:
  - Adicionar, visualizar, editar e deletar transações.
  - Filtragem de dados por mês e ano.
- **Interface Moderna**: Utiliza a biblioteca `ttkbootstrap` para um visual moderno e temas (claro/escuro).

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem**: Python 3
- **Interface Gráfica**:
  - `Tkinter` (biblioteca padrão do Python)
  - `ttkbootstrap` (para temas e widgets modernos)
- **Banco de Dados**:
  - `PostgreSQL` (utilizando o serviço NeonDB)
  - `psycopg2-binary` (driver de conexão)
- **Visualização de Dados**:
  - `matplotlib` (para a criação dos gráficos)
- **Outras Bibliotecas**:
  - `python-dotenv` (para gerenciamento de variáveis de ambiente)
  - `cryptography` (para criptografia de senhas)

---

## ⚙️ Pré-requisitos

Antes de começar, você vai precisar ter instalado em sua máquina:
- Python 3.10+
- Um banco de dados PostgreSQL. O projeto foi desenvolvido com NeonDB, que oferece um nível gratuito generoso.

---

## 🚀 Instalação e Execução

Siga os passos abaixo para executar o projeto localmente.

**1. Clone o repositório:**
```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

**2. Crie um ambiente virtual (recomendado):**
```bash
python -m venv venv
```
- No Windows:
  ```bash
  .\venv\Scripts\activate
  ```
- No macOS/Linux:
  ```bash
  source venv/bin/activate
  ```

**3. Instale as dependências:**
Crie um arquivo chamado `requirements.txt` na raiz do projeto com o seguinte conteúdo:
```txt
ttkbootstrap
matplotlib
psycopg2-binary
python-dotenv
cryptography
```
Em seguida, instale os pacotes com o comando:
```bash
pip install -r requirements.txt
```

**4. Configure as variáveis de ambiente:**
Crie um arquivo chamado `.env` na raiz do projeto e adicione a senha do seu banco de dados:
```
DB_PASSWORD="SUA_SENHA_DO_BANCO_DE_DADOS_AQUI"
```
*A chave de criptografia (`FERNET_KEY`) será gerada e salva automaticamente na primeira vez que a aplicação for executada.*

**5. Execute a aplicação:**
```bash
python main.py
```

---

Pronto! A aplicação deverá iniciar na tela de login.