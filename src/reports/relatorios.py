from conexion.mongo_queries import MongoQueries
import pandas as pd
from pymongo import ASCENDING, DESCENDING

class Relatorio:
    def __init__(self):
        pass

    def get_relatorio_hospedes(self):

        mongo = MongoQueries()
        mongo.connect()

        query_result = mongo.db["hospedes"].find({}, 
                                                 {"id_hospede": 1, 
                                                  "nome": 1, 
                                                  "sobrenome": 1,
                                                  "documento": 1,
                                                  "email": 1,
                                                  "_id": 0
                                                 }).sort("nome", ASCENDING)
        
        df_hospede = pd.DataFrame(list(query_result))
        mongo.close()
        print(df_hospede)
        input("Pressione Enter para Sair do Relatório de Hóspedes")

    def get_relatorio_tipos_quartos(self):
        # Relatório Simples
        mongo = MongoQueries()
        mongo.connect()

        query_result = mongo.db["tipos_quartos"].find({}, 
                                                      {"nome": 1, 
                                                       "descricao": 1, 
                                                       "preco_diaria": 1, 
                                                       "capacidade": 1,
                                                       "_id": 0
                                                      }).sort("nome", ASCENDING)
        
        df_tipos = pd.DataFrame(list(query_result))
        mongo.close()
        print(df_tipos)
        input("Pressione Enter para Sair do Relatório de Tipos de Quartos")

    def get_relatorio_quartos(self):

        mongo = MongoQueries()
        mongo.connect()
        
        query_result = mongo.db["quartos"].aggregate([
            {

                "$lookup": {
                    "from": "tipos_quartos",
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
                    "tipo": "$tipo.nome",           # Pega o nome do tipo
                    "preco": "$tipo.preco_diaria",  # Pega o preço do tipo
                    "_id": 0
                }
            },
            {
                "$sort": { "numero_quarto": 1 }
            }
        ])
        
        df_quartos = pd.DataFrame(list(query_result))
        mongo.close()
        print(df_quartos)
        input("Pressione Enter para Sair do Relatório de Quartos")

    def get_relatorio_reservas(self):
        # Relatório Complexo (Reserva + Hóspede + Quarto)
        mongo = MongoQueries()
        mongo.connect()
        
        query_result = mongo.db["reservas"].aggregate([
            {
                "$lookup": {
                    "from": "hospedes",
                    "localField": "id_hospede",
                    "foreignField": "id_hospede",
                    "as": "hospede"
                }
            },
            { "$unwind": { "path": "$hospede", "preserveNullAndEmptyArrays": True } },
            {
                "$lookup": {
                    "from": "quartos",
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
        
        df_reservas = pd.DataFrame(list(query_result))
        mongo.close()
        print(df_reservas)
        input("Pressione Enter para Sair do Relatório de Reservas")

    def get_relatorio_pagamentos(self):
        mongo = MongoQueries()
        mongo.connect()
        
        query_result = mongo.db["pagamentos"].aggregate([
            {
                "$lookup": {
                    "from": "reservas",
                    "localField": "id_reserva",
                    "foreignField": "id_reserva",
                    "as": "reserva"
                }
            },
            { "$unwind": { "path": "$reserva", "preserveNullAndEmptyArrays": True } },
            {
                "$lookup": {
                    "from": "hospedes",
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
        
        df_pagamentos = pd.DataFrame(list(query_result))
        mongo.close()
        print(df_pagamentos)
        input("Pressione Enter para Sair do Relatório de Pagamentos")

    def get_total_reservas_por_hospede(self):
        mongo = MongoQueries()
        mongo.connect()
        
        query_result = mongo.db["reservas"].aggregate([
            {
                "$group": {
                    "_id": "$id_hospede", 
                    "total_gasto": { "$sum": "$valor_total" },
                    "qtd_reservas": { "$sum": 1 }
                }
            },
            {
          
                "$lookup": {
                    "from": "hospedes",
                    "localField": "_id",
                    "foreignField": "id_hospede",
                    "as": "hospede"
                }
            },
            { "$unwind": "$hospede" },
            {
                "$project": {
                    "hospede": "$hospede.nome",
                    "total_reservas": "$qtd_reservas",
                    "total_gasto": 1,
                    "_id": 0
                }
            },
            { "$sort": { "total_gasto": -1 } }
        ])
        
        df_total = pd.DataFrame(list(query_result))
        mongo.close()
        print(df_total)
        input("Pressione Enter para Sair do Relatório de Totais")