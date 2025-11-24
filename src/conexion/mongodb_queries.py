import json
from urllib.parse import quote_plus
from pathlib import Path
import pymongo

class MongoDBConnection:
    def __init__(self, config_file="config/config.json"):
        self.client = None
        self.db = None
        self.config_file = config_file

        # Carrega o config (ou cria template se não existir)
        self.config = self._carregar_config()

    def connect(self):
        uri = self._get_uri()
        db_name = self.config["database"]["db_name"]

        self.client = pymongo.MongoClient(uri)
        self.db = self.client[db_name]
        return self.db

    def close(self):
        if self.client:
            self.client.close()
            self.client = None
            
    def get_db(self):
        return self.db

    def _carregar_config(self):
        # Define o caminho relativo a este arquivo
        config_path = Path(__file__).parent / self.config_file

        if not config_path.exists():
            self._criar_config_template(config_path)
            raise FileNotFoundError(f"""
Arquivo '{self.config_file}' não encontrado!
Um arquivo modelo foi criado automaticamente em '{config_path}'.

PASSO A PASSO PARA CONFIGURAR:
1. Edite o arquivo e coloque suas credenciais.
2. Se for local sem senha, deixe username e password vazios ("").
3. Rode o programa novamente.
            """)

        with open(config_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    def _criar_config_template(self, config_path):
        config_path.parent.mkdir(parents=True, exist_ok=True)

        modelo = {
            "database": {
                "username": "",
                "password": "",
                "host": "localhost",
                "port": 27017,
                "authSource": "admin",
                "db_name": "HOTEL_DB"
            }
        }

        with open(config_path, 'w', encoding='utf-8') as file:
            json.dump(modelo, file, ensure_ascii=False, indent=4)

    def _validar_config(self):
        db = self.config["database"]

        # CORREÇÃO: Removido username e password da lista de obrigatórios
        obrigatorios = ["host", "port", "authSource", "db_name"]

        faltando = [k for k in obrigatorios if not db.get(k)]
        if faltando:
            raise ValueError(f"""
ERRO: Os seguintes campos estão faltando no config.json:
{faltando}  
Estes campos são obrigatórios para conectar ao MongoDB.
""")

    def _get_uri(self):
        self._validar_config()
        db = self.config["database"]
        
        host = db["host"]
        port = db["port"]
        
        # Se não tiver usuário definido, conecta direto (comum em localhost)
        # Aceita string vazia "" ou chave inexistente ou valor "seu_usuario" (template)
        username = db.get("username", "")
        
        if not username or username == "seu_usuario":
            return f"mongodb://{host}:{port}/"
        
        # Se tiver usuário, usa autenticação
        user = quote_plus(username)
        pwd = quote_plus(db.get("password", ""))
        auth_db = db["authSource"]
        
        return