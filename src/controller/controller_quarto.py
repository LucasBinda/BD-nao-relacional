from bson import ObjectId
import pandas as pd
from model.quarto import quarto
from conexion.mongo_queries import MongoQueries

class Controller_Quarto:
    def __init__(self):
        self.mongo = MongoQueries()

    def inserir_quarto(self) -> Quarto:
        # Cria uma nova conexão com o banco
        self.mongo.connect()

        # Solicita ao usuario os novos dados do quarto
        numero_quarto = int(input("Número do Quarto (Novo): "))
        andar_quarto = int(input("Andar do Quarto (Novo): "))
        id_tipo_quarto = int(input("ID do Tipo de Quarto: "))
        status = input("Status do Quarto (Novo): ")

        # Recupera o próximo ID de quarto
        proximo_quarto = self.mongo.db["quartos"].aggregate([
            {
                '$group': {
                    '_id': '$quartos',
                    'proximo_quarto': {
                        '$max': '$id_quarto'
                    }
                }
            }, {
                '$project': {
                    'proximo_quarto': {
                        '$sum': [
                            '$proximo_quarto', 1
                        ]
                    },
                    '_id': 0
                }
            }
        ])

        proximo_quarto = int(list(proximo_quarto)[0]['proximo_quarto'])

        # Insere e Recupera o ID do novo quarto
        id_quarto = self.mongo.db["quartos"].insert_one({
            "id_quarto": proximo_quarto,
            "numero_quarto": numero_quarto,
            "andar_quarto": andar_quarto,
            "id_tipo_quarto": id_tipo_quarto,
            "status": status
        })

        # Recupera os dados do novo quarto criado transformando em um DataFrame
        df_quarto = self.recupera_quarto(id_quarto.inserted_id)

        # Cria um novo objeto Quarto
        novo_quarto = Quarto(
            df_quarto.id_quarto.values[0],
            df_quarto.numero_quarto.values[0],
            df_quarto.andar_quarto.values[0],
            df_quarto.id_tipo_quarto.values[0],
            df_quarto.status.values[0]
        )

        # Exibe os atributos do novo quarto
        print(novo_quarto.to_string())
        self.mongo.close()

        # Retorna o objeto novo_quarto
        return novo_quarto

    def atualizar_quarto(self) -> Quarto:
        # Cria uma nova conexão com o banco que permite alteração
        self.mongo.connect()

        # Solicita ao usuário o ID do quarto a ser alterado
        id_quarto = int(input("ID do Quarto que irá alterar: "))

        # Verifica se o quarto existe na base de dados
        if not self.verifica_existencia_quarto(id_quarto):
            # Solicita os novos dados do quarto
            numero_quarto = int(input("Número do Quarto (Novo): "))
            andar_quarto = int(input("Andar (Novo): "))
            id_tipo_quarto = int(input("ID do Tipo de Quarto (Novo): "))
            status = input("Status (Novo): ")

            # Atualiza o quarto existente
            self.mongo.db["quartos"].update_one(
                {"id_quarto": id_quarto},
                {"$set": {
                    "numero_quarto": numero_quarto,
                    "andar_quarto": andar_quarto,
                    "id_tipo_quarto": id_tipo_quarto,
                    "status": status
                }}
            )

            # Recupera os dados do quarto atualizado
            df_quarto = self.recupera_quarto_codigo(id_quarto)

            # Cria o objeto quarto atualizado
            quarto_atualizado = Quarto(
                df_quarto.id_quarto.values[0],
                df_quarto.numero_quarto.values[0],
                df_quarto.andar_quarto.values[0],
                df_quarto.id_tipo_quarto.values[0],
                df_quarto.status.values[0]
            )

            # Exibe os atributos do quarto atualizado
            print(quarto_atualizado.to_string())
            self.mongo.close()
            return quarto_atualizado

        else:
            self.mongo.close()
            print(f"O quarto ID {id_quarto} não existe.")
            return None

    def excluir_quarto(self):
        # Cria uma nova conexão com o banco que permite alteração
        self.mongo.connect()

        # Solicita o ID do quarto a ser excluído
        id_quarto = int(input("ID do Quarto que irá excluir: "))

        # Verifica se o quarto existe na base de dados
        if not self.verifica_existencia_quarto(id_quarto):
            # Recupera os dados do quarto antes da exclusão
            df_quarto = self.recupera_quarto_codigo(id_quarto)

            # Remove o quarto da tabela
            self.mongo.db["quartos"].delete_one({"id_quarto": id_quarto})

            # Cria objeto representando o quarto excluído
            quarto_excluido = Quarto(
                df_quarto.id_quarto.values[0],
                df_quarto.numero_quarto.values[0],
                df_quarto.andar_quarto.values[0],
                df_quarto.id_tipo_quarto.values[0],
                df_quarto.status.values[0]
            )

            # Exibe mensagem de sucesso e os dados excluídos
            print("Quarto Removido com Sucesso!")
            print(quarto_excluido.to_string())
            self.mongo.close()

        else:
            self.mongo.close()
            print(f"O quarto ID {id_quarto} não existe.")

    def verifica_existencia_quarto(self, id_quarto:int=None, external: bool = False) -> bool:
        if external:
            # Cria uma nova conexão com o banco que permite alteração
            self.mongo.connect()

        # Recupera o quarto a partir do ID informado
        df_quarto = pd.DataFrame(self.mongo.db["quartos"].find(
            {"id_quarto": id_quarto},
            {"id_quarto": 1, "_id": 0}
        ))

        if external:
            # Fecha a conexão com o Mongo
            self.mongo.close()

        return df_quarto.empty

    def recupera_quarto(self, _id:ObjectId=None) -> pd.DataFrame:
        # Recupera os dados do novo quarto criado transformando em um DataFrame
        df_quarto = pd.DataFrame(list(self.mongo.db["quartos"].find(
            {"_id": _id},
            {"id_quarto": 1, "numero_quarto": 1, "andar_quarto": 1, "id_tipo_quarto": 1, "status": 1, "_id": 0}
        )))
        return df_quarto

    def recupera_quarto_codigo(self, id_quarto:int=None, external: bool = False) -> pd.DataFrame:
        if external:
            # Cria uma nova conexão com o banco que permite alteração
            self.mongo.connect()

        # Recupera os dados do quarto existente transformando em um DataFrame
        df_quarto = pd.DataFrame(list(self.mongo.db["quartos"].find(
            {"id_quarto": id_quarto},
            {"id_quarto": 1, "numero_quarto": 1, "andar_quarto": 1, "id_tipo_quarto": 1, "status": 1, "_id": 0}
        )))

        if external:
            # Fecha a conexão com o Mongo
            self.mongo.close()

        return df_quarto
