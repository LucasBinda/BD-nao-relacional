import logging
import json
import pandas as pd
from conexion.mongodb_queries import MongoDBConnection 
from conexion.oracle_queries import OracleQueries

# --- LISTA DAS TABELAS DO PROJETO HOTELARIA ---
# Estas coleções serão criadas no MongoDB, conforme solicitado.
LIST_OF_COLLECTIONS = ["hospede", "tipo_quarto", "quarto", "reserva", "pagamento"] 

# Configuração de Log
logger = logging.getLogger(name="MongoDataMigrator")
logger.setLevel(level=logging.WARNING)

def create_collections(mongo_conn: MongoDBConnection, drop_if_exists:bool=False):
    """
    Cria as coleções no MongoDB. Se drop_if_exists for True, apaga e recria.
    Atende ao Requisito IV.
    """
    mongo_conn.connect()
    db = mongo_conn.get_db()
    
    existing_collections = db.list_collection_names()
    
    for collection in LIST_OF_COLLECTIONS:
        if collection in existing_collections:
            if drop_if_exists:
                db.drop_collection(collection)
                logger.warning(f"Coleção '{collection}' removida!")
                db.create_collection(collection)
                logger.warning(f"Coleção '{collection}' criada!")
        else:
            db.create_collection(collection)
            logger.warning(f"Coleção '{collection}' criada!")
            
    mongo_conn.close()

def insert_many(mongo_conn: MongoDBConnection, data:list, collection:str):
    """
    Insere múltiplos documentos na coleção especificada.
    """
    mongo_conn.connect()
    db = mongo_conn.get_db()
    db[collection].insert_many(data)
    mongo_conn.close()

def migrate_data():
    """
    Extrai dados do Oracle (Requisito V), converte para JSON/Documentos e insere no MongoDB.
    """
    oracle = OracleQueries()
    oracle.connect()
    
    # Instancia MongoDBConnection (Requisito III)
    mongo_conn = MongoDBConnection() 
    
    sql = "select * from {table}" # Query de extração
    
    # --- Passo 1: Criar/Limpar as Coleções ---
    create_collections(mongo_conn=mongo_conn, drop_if_exists=True)
    
    # --- Passo 2: Extrair e Inserir ---
    for collection in LIST_OF_COLLECTIONS:
        try:
            # 1. Extração do Oracle
            df = oracle.sqlToDataFrame(sql.format(table=collection))
            
            # 2. Conversão de tipos (Pandas para JSON)
            # orient='records' gera o formato [{}, {}, ...] ideal para o MongoDB
            # date_format='iso' garante que datas sejam serializadas corretamente
            records = json.loads(df.to_json(orient='records', date_format='iso'))
            
            logger.warning(f"Dados extraídos da tabela Oracle {collection}")
            
            # 3. Inserção no MongoDB (Requisito V)
            insert_many(mongo_conn=mongo_conn, data=records, collection=collection)
            logger.warning(f"Documentos gerados na coleção {collection}")
            
        except Exception as e:
             logger.error(f"Erro ao migrar a coleção {collection}: {e}")
             
    oracle.close()


if __name__ == "__main__":
    # NOTA: O arquivo src/conexion/mongodb_queries.py precisa de um arquivo de configuração config/config.json 
    # com as credenciais do seu MongoDB antes de rodar este script.
    logging.warning("Starting MongoDB Migration")
    migrate_data() 
    logging.warning("End of MongoDB Migration")