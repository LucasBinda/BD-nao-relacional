import json
import pymongo
from urllib.parse import quote_plus
from pathlib import Path


class MongoDBConnection:
    def __init__(self, config_file="config/config.json"):
        self.client = None
        self.db = None
        self.config_file = config_file

        # Carrega o config (ou cria template se não existir)
        self.config = self._carregar_config()

    def connect(self): # 5. abre conexão com o MongoClient
        uri = self._get_uri()
        db_name = self.config["database"]["db_name"]

        self.client = pymongo.MongoClient(uri)
        self.db = self.client[db_name]
        return self.db


    def close(self): # 6. Fecha conexão
        if self.client:
            self.client.close()
            self.client = None

    def _carregar_config(self): # 1. Carrega config.json
        config_path = Path(__file__).parent / self.config_file

        if not config_path.exists():
            self._criar_config_template(config_path)
            raise FileNotFoundError(f"""
Arquivo '{self.config_file}' não encontrado!
Um arquivo modelo foi criado automaticamente.

PASSO A PASSO PARA CONFIGURAR:
1. Edite '{self.config_file}' com suas credenciais reais.
2. authSource deve ser o banco ONDE O USUÁRIO FOI CRIADO.
3. Depois rode o programa novamente.
            """)

        with open(config_path, 'r', encoding='utf-8') as file:
            return json.load(file)


    def _criar_config_template(self, config_path): # 2. Cria template config.json se não existir
        config_path.parent.mkdir(parents=True, exist_ok=True)

        modelo = {
            "database": {
                "username": "seu_usuario",
                "password": "sua_senha",
                "host": "localhost",
                "port": 27017,
                "authSource": "admin",
                "db_name": "meu_banco"
            }
        }

        with open(config_path, 'w', encoding='utf-8') as file:
            json.dump(modelo, file, ensure_ascii=False, indent=4)


    def _validar_config(self): # 3. Validação simples
        db = self.config["database"]

        obrigatorios = ["username", "password", "host", "port", "authSource", "db_name"]

        faltando = [k for k in obrigatorios if not db.get(k)]
        if faltando:
            raise ValueError(f"""
ERRO: Os seguintes campos estão faltando no config.json:
{faltando}  
Todos são obrigatórios para conectar ao MongoDB.
""")


    def _get_uri(self): # 4. Gera a MongoDB URI sempre com authSource
        self._validar_config()

        db = self.config["database"]

        user = quote_plus(db["username"])
        pwd = quote_plus(db["password"])
        host = db["host"]
        port = db["port"]
        auth_db = db["authSource"]

        # authSource sempre explícito
        return f"mongodb://{user}:{pwd}@{host}:{port}/?authSource={auth_db}"


