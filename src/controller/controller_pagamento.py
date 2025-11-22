from bson import ObjectId
import pandas as pd
from model.pagamento import pagamento
from conexion.mongo_queries import MongoQueries
from datetime import date

class Controller_Pagamento:
    def __init__(self):
        self.mongo = MongoQueries()

    def inserir_pagamento(self) -> Pagamento:
        # Cria uma nova conexão com o banco
        self.mongo.connect()

        #Solicita ao usuario os novos dados do pagamento
        id_reserva = int(input("ID da Reserva: "))
        valor_pago = float(input("Valor Pago: "))
        data_pagamento = input("Data do Pagamento (AAAA-MM-DD): ")
        data_pagamento = date.fromisoformat(data_pagamento)
        metodo = input("Método de Pagamento: ")
        status = input("Status do Pagamento: ")

        # Recupera o próximo id_pagamento
        proximo_pagamento = self.mongo.db["pagamentos"].aggregate([
            {
                '$group': {
                    '_id': '$pagamentos',
                    'proximo_pagamento': {
                        '$max': '$id_pagamento'
                    }
                }
            }, {
                '$project': {
                    'proximo_pagamento': {
                        '$sum': [
                            '$proximo_pagamento', 1
                        ]
                    },
                    '_id': 0
                }
            }
        ])

        proximo_pagamento = int(list(proximo_pagamento)[0]['proximo_pagamento'])

        # Insere e Recupera o id do novo pagamento
        id_pagamento = self.mongo.db["pagamentos"].insert_one({
            "id_pagamento": proximo_pagamento,
            "id_reserva": id_reserva,
            "valor_pago": valor_pago,
            "data_pagamento": str(data_pagamento),
            "metodo": metodo,
            "status": status
        })

        # Recupera os dados do novo pagamento criado transformando em um DataFrame
        df_pagamento = self.recupera_pagamento(id_pagamento.inserted_id)

        # Cria um novo objeto Pagamento
        novo_pagamento = Pagamento(
            df_pagamento.id_pagamento.values[0],
            df_pagamento.id_reserva.values[0],
            df_pagamento.valor_pago.values[0],
            df_pagamento.data_pagamento.values[0],
            df_pagamento.metodo.values[0],
            df_pagamento.status.values[0]
        )

        # Exibe os atributos do novo pagamento
        print(novo_pagamento.to_string())
        self.mongo.close()
        return novo_pagamento

    def atualizar_pagamento(self) -> Pagamento:
        # Cria uma nova conexão com o banco que permite alteração
        self.mongo.connect()

        # Solicita ao usuário o ID do pagamento a ser alterado
        id_pagamento = int(input("ID do Pagamento que irá alterar: "))

        # Verifica se o pagamento existe na base de dados
        if not self.verifica_existencia_pagamento(id_pagamento):
            # Solicita os novos dados
            valor_pago = float(input("Novo Valor Pago: "))
            data_pagamento = input("Nova Data do Pagamento (AAAA-MM-DD): ")
            data_pagamento = date.fromisoformat(data_pagamento)
            metodo = input("Novo Método de Pagamento: ")
            status = input("Novo Status do Pagamento: ")

            # Atualiza o pagamento existente
            self.mongo.db["pagamentos"].update_one(
                {"id_pagamento": id_pagamento},
                {"$set": {
                    "valor_pago": valor_pago,
                    "data_pagamento": str(data_pagamento),
                    "metodo": metodo,
                    "status": status
                }}
            )

            # Recupera os dados do pagamento atualizado
            df_pagamento = self.recupera_pagamento_codigo(id_pagamento)

            # Cria um novo objeto Pagamento
            pagamento_atualizado = Pagamento(
                df_pagamento.id_pagamento.values[0],
                df_pagamento.id_reserva.values[0],
                df_pagamento.valor_pago.values[0],
                df_pagamento.data_pagamento.values[0],
                df_pagamento.metodo.values[0],
                df_pagamento.status.values[0]
            )

            # Exibe os atributos do novo pagamento
            print(pagamento_atualizado.to_string())
            self.mongo.close()
            return pagamento_atualizado
        else:
            self.mongo.close()
            print(f"O pagamento ID {id_pagamento} não existe.")
            return None

    def excluir_pagamento(self):
        # Cria uma nova conexão com o banco que permite alteração
        self.mongo.connect()

        # Solicita ao usuário o ID do pagamento que irá excluir
        id_pagamento = int(input("ID do Pagamento que irá excluir: "))

        # Verifica se o pagamento existe na base de dados
        if not self.verifica_existencia_pagamento(id_pagamento):
            # Recupera os dados do pagamento a ser excluído
            df_pagamento = self.recupera_pagamento_codigo(id_pagamento)

            # Revome o pagamento da tabela
            self.mongo.db["pagamentos"].delete_one({"id_pagamento": id_pagamento})

            # Cria um novo objeto Pagamento para informar que foi removido
            pagamento_excluido = Pagamento(
                df_pagamento.id_pagamento.values[0],
                df_pagamento.id_reserva.values[0],
                df_pagamento.valor_pago.values[0],
                df_pagamento.data_pagamento.values[0],
                df_pagamento.metodo.values[0],
                df_pagamento.status.values[0]
            )

            print("Pagamento Removido com Sucesso!")
            print(pagamento_excluido.to_string())
            self.mongo.close()
        else:
            self.mongo.close()
            print(f"O pagamento ID {id_pagamento} não existe.")

    def verifica_existencia_pagamento(self, id_pagamento:int=None, external: bool = False) -> bool:
        if external:
            # Cria uma nova conexão com o banco que permite alteração
            self.mongo.connect()

        # Recupera os dados do pagamento transformando em um DataFrame
        df_pagamento = pd.DataFrame(
            self.mongo.db["pagamentos"].find(
                {"id_pagamento": id_pagamento},
                {"id_pagamento": 1, "_id": 0}
            )
        )

        if external:
            # Fecha a conexão com o Mongo
            self.mongo.close()

        return df_pagamento.empty

    def recupera_pagamento(self, _id:ObjectId=None) -> pd.DataFrame:
        # Recupera os dados do pagamento transformando em um DataFrame
        df_pagamento = pd.DataFrame(list(
            self.mongo.db["pagamentos"].find(
                {"_id": _id},
                {"id_pagamento":1,"id_reserva":1,"valor_pago":1,"data_pagamento":1,"metodo":1,"status":1,"_id":0}
            )
        ))
        return df_pagamento

    def recupera_pagamento_codigo(self, id_pagamento:int=None, external: bool = False) -> pd.DataFrame:
        if external:
            # Cria uma nova conexão com o banco que permite alteração
            self.mongo.connect()

        # Recupera os dados do pagamento transformando em um DataFrame
        df_pagamento = pd.DataFrame(list(
            self.mongo.db["pagamentos"].find(
                {"id_pagamento": id_pagamento},
                {"id_pagamento":1,"id_reserva":1,"valor_pago":1,"data_pagamento":1,"metodo":1,"status":1,"_id":0}
            )
        ))

        if external:
            # Fecha a conexão com o Mongo
            self.mongo.close()

        return df_pagamento
