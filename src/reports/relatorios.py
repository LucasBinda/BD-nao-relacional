from conexion.mongo_queries import MongoQueries
import pandas as pd
from pymongo import ASCENDING, DESCENDING

class Relatorio:
    def __init__(self):
        # Inicializa a instância de conexão no construtor
        self.mongo = MongoQueries()

    def get_relatorio_hospede(self):
        # Abre a conexão
        self.mongo.connect()

        # Realiza a consulta na coleção 'hospede'
        query_result = self.mongo.db["hospede"].find({}, 
                                                 {"id_hospede": 1, 
                                                  "nome": 1, 
                                                  "sobrenome": 1,
                                                  "documento": 1,
                                                  "email": 1,
                                                  "_id": 0
                                                 }).sort("nome", ASCENDING)
        
        # Converte para DataFrame
        df_hospede = pd.DataFrame(list(query_result))
        
        # Fecha a conexão
        self.mongo.close()
        
        # Exibe o resultado
        print(df_hospede)
        input("Pressione Enter para Sair do Relatório de Hóspede")

    def get_relatorio_tipo_quarto(self):
        self.mongo.connect()

        query_result = self.mongo.db["tipo_quarto"].find({}, 
                                                      {"nome": 1, 
                                                       "descricao": 1, 
                                                       "preco_diaria": 1, 
                                                       "capacidade": 1,
                                                       "_id": 0
                                                      }).sort("nome", ASCENDING)
        
        df_tipo = pd.DataFrame(list(query_result))
        self.mongo.close()
        print(df_tipo)
        input("Pressione Enter para Sair do Relatório de Tipo de Quarto")

    def get_relatorio_quarto(self):
        self.mongo.connect()
        
        query_result = self.mongo.db["quarto"].aggregate([
            {
                "$lookup": {
                    "from": "tipo_quarto",
                    "localField": "id_tipo_quarto",
                    "foreignField": "id_tipo_quarto",
                    "as": "tipo"
                }
            },
            {
                "$unwind": { "path": "$tipo", "preserveNullAndEmptyArrays": True }
            },
            {
                "$project": {
                    "numero_quarto": 1,
                    "andar": 1,
                    "status": 1,
                    "tipo": "$tipo.nome",           
                    "preco": "$tipo.preco_diaria",  
                    "_id": 0
                }
            },
            {
                "$sort": { "numero_quarto": 1 }
            }
        ])
        
        df_quarto = pd.DataFrame(list(query_result))
        self.mongo.close()
        print(df_quarto)
        input("Pressione Enter para Sair do Relatório de Quarto")

    def get_relatorio_reserva(self):
        self.mongo.connect()
        
        query_result = self.mongo.db["reserva"].aggregate([
            {
                "$lookup": {
                    "from": "hospede",
                    "localField": "id_hospede",
                    "foreignField": "id_hospede",
                    "as": "hospede"
                }
            },
            { "$unwind": { "path": "$hospede", "preserveNullAndEmptyArrays": True } },
            {
                "$lookup": {
                    "from": "quarto",
                    "localField": "id_quarto",
                    "foreignField": "id_quarto",
                    "as": "quarto"
                }
            },
            { "$unwind": { "path": "$quarto", "preserveNullAndEmptyArrays": True } },
            {
                "$project": {
                    "id_reserva": 1,
                    "nome_hospede": "$hospede.nome",
                    "sobrenome_hospede": "$hospede.sobrenome",
                    "quarto": "$quarto.numero_quarto",
                    "checkin": "$data_checkin",
                    "checkout": "$data_checkout",
                    "total": "$valor_total",
                    "_id": 0
                }
            },
            { "$sort": { "checkin": 1 } }
        ])
        
        df_reserva = pd.DataFrame(list(query_result))
        self.mongo.close()
        print(df_reserva)
        input("Pressione Enter para Sair do Relatório de Reserva")

    def get_relatorio_pagamento(self):
        self.mongo.connect()
        
        query_result = self.mongo.db["pagamento"].aggregate([
            {
                "$lookup": {
                    "from": "reserva",
                    "localField": "id_reserva",
                    "foreignField": "id_reserva",
                    "as": "reserva"
                }
            },
            { "$unwind": { "path": "$reserva", "preserveNullAndEmptyArrays": True } },
            {
                "$lookup": {
                    "from": "hospede",
                    "localField": "reserva.id_hospede",
                    "foreignField": "id_hospede",
                    "as": "hospede"
                }
            },
            { "$unwind": { "path": "$hospede", "preserveNullAndEmptyArrays": True } },
            {
                "$project": {
                    "id_pagamento": 1,
                    "metodo": 1,
                    "valor": 1,
                    "data": "$data_pagamento",
                    "pagante": "$hospede.nome",
                    "_id": 0
                }
            }
        ])
        
        df_pagamento = pd.DataFrame(list(query_result))
        self.mongo.close()
        print(df_pagamento)
        input("Pressione Enter para Sair do Relatório de Pagamento")

    def get_total_reserva_por_hospede(self):
        self.mongo.connect()
        
        query_result = self.mongo.db["reserva"].aggregate([
            {
                "$group": {
                    "_id": "$id_hospede", 
                    "total_gasto": { "$sum": "$valor_total" },
                    "qtd_reserva": { "$sum": 1 }
                }
            },
            {
                "$lookup": {
                    "from": "hospede",
                    "localField": "_id",
                    "foreignField": "id_hospede",
                    "as": "hospede"
                }
            },
            { "$unwind": "$hospede" },
            {
                "$project": {
                    "hospede": "$hospede.nome",
                    "total_reserva": "$qtd_reserva",
                    "total_gasto": 1,
                    "_id": 0
                }
            },
            { "$sort": { "total_gasto": -1 } }
        ])
        
        df_total = pd.DataFrame(list(query_result))
        self.mongo.close()
        print(df_total)
        input("Pressione Enter para Sair do Relatório de Total Gasto por Hóspede")