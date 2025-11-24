

````markdown
# 🏨 Sistema de Gestão de Reservas Hoteleiras (NoSQL)

Este projeto implementa um sistema de gestão de reservas hoteleiras desenvolvido em **Python**, utilizando o banco de dados não relacional **MongoDB** para a persistência dos dados.

O sistema adota a arquitetura **MVC (Model-View-Controller)** e foi migrado de uma estrutura relacional para documentos, permitindo maior flexibilidade e escalabilidade.

---

## 🚀 Tecnologias Utilizadas

* **Linguagem:** Python 3.10+
* **Banco de Dados:** MongoDB
* **Driver:** PyMongo
* **Manipulação de Dados:** Pandas
* **Ambiente:** Linux / GitHub Codespaces

---

## 📋 Pré-requisitos

Para executar este projeto no Linux, certifique-se de ter instalado:

1.  **Python 3.8+**: `sudo apt-get install python3`
2.  **Git**: `sudo apt-get install git`
3.  **MongoDB**: Recomenda-se usar o **Docker** para rodar o banco de dados rapidamente sem instalações complexas.

---

## 🔧 Instalação e Configuração (Passo a Passo)

Siga os comandos abaixo no seu terminal para configurar o ambiente.

### 1. Clonar o Repositório

```bash
git clone [https://github.com/mikaellycardoso/banco-de-dados.git](https://github.com/mikaellycardoso/banco-de-dados.git)
cd banco-de-dados
````

### 2\. Configurar o Banco de Dados (Docker)

Se você ainda não tem o MongoDB rodando, suba um contêiner Docker com o comando:

```bash
# Baixa e inicia o MongoDB na porta padrão 27017
docker run -d -p 27017:27017 --name mongodb mongo:latest
```

*Para verificar se está rodando:* `docker ps`

### 3\. Configurar o Ambiente Virtual Python

É uma boa prática isolar as dependências do projeto.

```bash
# Cria o ambiente virtual chamado '.venv'
python3 -m venv .venv

# Ativa o ambiente virtual
source .venv/bin/activate
```

*(Você verá `(.venv)` no início da linha do terminal)*

### 4\. Instalar Dependências

Instale as bibliotecas necessárias (PyMongo, Pandas, etc.):

```bash
pip install -r src/requeriments.txt
```

-----

## ⚙️ Inicialização e Carga de Dados

O sistema precisa criar as coleções e inserir dados iniciais para funcionar.

### 1\. Gerar Arquivo de Configuração

Execute o script de população pela primeira vez para gerar o arquivo de configuração do banco:

```bash
python3 src/seed_mongo.py
```

  * O script tentará conectar. Se falhar (ou se for a primeira vez), ele criará o arquivo `src/conexion/config/config.json`.
  * **Nota:** Se você está usando o Docker localmente sem senha (comando acima), a configuração padrão já funcionará. Se precisar alterar usuário/senha, edite o arquivo `src/conexion/config/config.json`.

### 2\. Popular o Banco de Dados

Execute o script novamente para limpar o banco e inserir os dados de teste:

```bash
python3 src/seed_mongo.py
```

**Saída Esperada:**

> *Banco de dados MongoDB populado com sucesso\!*

-----

## ▶️ Como Rodar a Aplicação

Após a configuração, inicie o sistema principal:

```bash
python3 src/principal.py
```

### Funcionalidades Disponíveis no Menu:

1.  **Relatórios:** Visualize hóspedes, quartos e reservas cadastrados.
2.  **Inserir Registros:** Cadastre novos hóspedes ou reservas.
3.  **Atualizar/Remover:** Gerencie os registros existentes.

-----

## 📂 Estrutura do Projeto

```
/
├── src/
│   ├── conexion/          # Conexão com MongoDB
│   │   ├── config/        # Configuração (config.json)
│   │   └── mongodb_queries.py
│   ├── controller/        # Lógica de Negócio
│   ├── model/             # Classes (Hospede, Reserva, etc.)
│   ├── reports/           # Relatórios com Pandas
│   ├── utils/             # Menus e Splash Screen
│   ├── principal.py       # Arquivo Principal
│   └── seed_mongo.py      # Script de População (Seed)
├── requirements.txt       # Lista de Dependências
└── README.md              # Documentação
```

-----

## 👥 Autores

  * **Anna Luiza, Laisa Camilo, Lucas Binda, Mikaelly Cardoso, Victória Teixeira**

<!-- end list -->

```
```