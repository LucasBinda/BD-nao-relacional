````markdown
# 🏨 Sistema de Gestão de Reservas Hoteleiras (NoSQL)

Este projeto consiste em um sistema de gerenciamento de reservas hoteleiras desenvolvido em **Python**, utilizando o banco de dados não relacional **MongoDB** para a persistência de todos os dados.

O sistema foi migrado de uma arquitetura relacional para NoSQL e segue o padrão **MVC (Model-View-Controller)**.

---

## 🚀 Funcionalidades

O sistema oferece um menu interativo via terminal para gerenciamento completo das seguintes entidades:

* **Hóspedes:** Cadastro, atualização e remoção de clientes.
* **Tipos de Quarto:** Gerenciamento das categorias e preços.
* **Quartos:** Controle dos quartos físicos e seus status.
* **Reservas:** Criação de novas reservas com validação de disponibilidade.
* **Pagamentos:** Registro de pagamentos associados às reservas.

Além das operações de CRUD (Create, Read, Update, Delete), o sistema gera **Relatórios Gerenciais** detalhados.

---

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3.10+
* **Banco de Dados:** MongoDB
* **Driver:** PyMongo
* **Manipulação de Dados:** Pandas
* **Ambiente de Desenvolvimento:** VS Code / GitHub Codespaces

---

## 📦 Estrutura do Projeto

```text
/
├── src/
│   ├── conexion/           # Conexão com o MongoDB
│   │   ├── config/         # Arquivo de configuração (config.json)
│   │   └── mongodb_queries.py
│   ├── controller/         # Controladores (Lógica de Negócio)
│   │   ├── controller_hospede.py
│   │   ├── controller_reserva.py
│   │   └── ...
│   ├── model/              # Classes de Modelo (POO)
│   │   ├── Hospede.py
│   │   ├── Reserva.py
│   │   └── ...
│   ├── reports/            # Relatórios Gerenciais
│   │   └── relatorios.py
│   ├── utils/              # Utilitários (Menus, Splash Screen)
│   ├── principal.py        # Arquivo Principal (Main)
│   └── seed_mongo.py       # Script de População do Banco
├── requirements.txt        # Dependências do Python
└── README.md               # Documentação
````

-----

## 🔧 Como Executar o Projeto

### 1\. Pré-requisitos

Certifique-se de ter o **Python** e o **MongoDB** instalados.

  * **Se estiver usando Docker (Recomendado):**
    ```bash
    docker run -d -p 27017:27017 --name mongodb mongo:latest
    ```

### 2\. Configuração do Ambiente

Clone o repositório e instale as dependências:

```bash
# Clone o projeto
git clone [https://github.com/seu-usuario/seu-repositorio.git](https://github.com/seu-usuario/seu-repositorio.git)
cd banco-de-dados

# Crie e ative o ambiente virtual (Opcional, mas recomendado)
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# Instale as bibliotecas
pip install -r src/requeriments.txt
```

### 3\. Configuração do Banco de Dados

O sistema precisa de um arquivo de configuração para conectar ao MongoDB.

1.  Execute o script de população (`seed_mongo.py`) pela primeira vez. Ele criará automaticamente o arquivo `src/conexion/config/config.json`.
2.  Se necessário, edite o arquivo `config.json` com suas credenciais (para conexão local sem senha, deixe os campos vazios).

### 4\. Inicialização (Seed)

Para criar as coleções e inserir dados de teste, execute:

```bash
python src/seed_mongo.py
```

*Isso limpará o banco atual e inserirá registros de exemplo para Hóspedes, Quartos e Reservas.*

### 5\. Execução

Inicie o sistema principal:

```bash
python src/principal.py
```

-----

## 👥 Autores

  * **Anna Luiza, Laisa Camilo, Lucas Binda, Mikaelly Cardoso, Victória Teixeira**

<!-- end list -->

```
```