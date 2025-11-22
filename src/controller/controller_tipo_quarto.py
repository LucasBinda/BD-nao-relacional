from bson import ObjectId
import pandas as pd
from model.tipo_quarto import tipo_quarto
from conexion.mongo_queries import MongoQueries
import decimal

class Controller_TipoQuarto:
    def __init__(self):
        self.mongo = MongoQueries()

    def inserir_tipo_quarto(self) -> tipo_quarto:
        # Cria uma nova conexão com o banco
        self.mongo.connect()

        #Solicita ao usuario os novos dados do tipo de quarto
        nome_tipo = input("Nome do Tipo de Quarto (Novo): ")
        descricao_tipo = input("Descrição (Nova): ")
        capacidade_maxima = int(input("Capacidade Máxima (Nova): "))
        preco_diaria = decimal.Decimal(input("Preço da Diária (Nova): "))

        # Recupera o próximo ID de tipo de quarto (simulando sequence)
        proximo_tipo = self.mongo.db["tipo_quarto"].aggregate([
            {
                '$group': {
                    '_id': '$tipo_quarto',
                    'proximo_tipo': {
                        '$max': '$id_tipo_quarto'
                    }
                }
            }, {
                '$project': {
                    'proximo_tipo': {
                        '$sum': [
                            '$proximo_tipo', 1
                        ]
                    },
                    '_id': 0
                }
            }
        ])

        proximo_tipo = int(list(proximo_tipo)[0]['proximo_tipo'])

        # Insere e Recupera o ID do novo tipo de quarto
        id_tipo = self.mongo.db["tipo_quarto"].insert_one({
            "id_tipo_quarto": proximo_tipo,
            "nome_tipo": nome_tipo,
            "descricao_tipo": descricao_tipo,
            "capacidade_maxima": capacidade_maxima,
            "preco_diaria": float(preco_diaria)
        })

        # Recupera os dados do novo tipo de quarto criado transformando em um DataFrame
        df_tipo = self.recupera_tipo(id_tipo.inserted_id)

        # Cria um novo objeto tipo_quarto
        novo_tipo = tipo_quarto(
            df_tipo.id_tipo_quarto.values[0],
            df_tipo.nome_tipo.values[0],
            df_tipo.descricao_tipo.values[0],
            df_tipo.capacidade_maxima.values[0],
            df_tipo.preco_diaria.values[0]
        )

        # Exibe os atributos do novo tipo de quarto
        print(novo_tipo.to_string())
        self.mongo.close()

        # Retorna o objeto novo_tipo para utilização posterior, caso necessário
        return novo_tipo

    def atualizar_tipo_quarto(self) -> tipo_quarto:
        # Cria uma nova conexão com o banco que permite alteração
        self.mongo.connect()

        # Solicita ao usuário o ID do tipo de quarto a ser alterado
        id_tipo_quarto = int(input("ID do Tipo de Quarto que irá alterar: "))

        # Verifica se o tipo de quarto existe na base de dados
        if not self.verifica_existencia_tipo_quarto(id_tipo_quarto):
            # Solicita os novos dados
            nome_tipo = input("Nome do Tipo de Quarto (Novo): ")
            descricao_tipo = input("Descrição (Nova): ")
            capacidade_maxima = int(input("Capacidade Máxima (Nova): "))
            preco_diaria = decimal.Decimal(input("Preço da Diária (Nova): "))

            # Atualiza os dados do tipo de quarto existente
            self.mongo.db["tipo_quarto"].update_one(
                {"id_tipo_quarto": id_tipo_quarto},
                {
                    "$set": {
                        "nome_tipo": nome_tipo,
                        "descricao_tipo": descricao_tipo,
                        "capacidade_maxima": capacidade_maxima,
                        "preco_diaria": float(preco_diaria)
                    }
                }
            )

            # Recupera os dados do tipo de quarto atualizado
            df_tipo = self.recupera_tipo_codigo(id_tipo_quarto)

            # Cria um novo objeto tipo_quarto
            tipo_atualizado = tipo_quarto(
                df_tipo.id_tipo_quarto.values[0],
                df_tipo.nome_tipo.values[0],
                df_tipo.descricao_tipo.values[0],
                df_tipo.capacidade_maxima.values[0],
                df_tipo.preco_diaria.values[0]
            )

            # Exibe os atributos atualizados
            print(tipo_atualizado.to_string())
            self.mongo.close()

            # Retorna o objeto atualizado para uso posterior
            return tipo_atualizado
        else:
            self.mongo.close()
            print(f"O tipo de quarto ID {id_tipo_quarto} não existe.")
            return None

    def excluir_tipo_quarto(self):
        # Cria uma nova conexão com o banco que permite alteração
        self.mongo.connect()

        # Solicita ao usuário o ID do tipo de quarto a ser excluído
        id_tipo_quarto = int(input("ID do Tipo de Quarto que irá excluir: "))

        # Verifica se o tipo de quarto existe na base de dados
        if not self.verifica_existencia_tipo_quarto(id_tipo_quarto):
            # Recupera os dados do tipo de quarto antes da exclusão
            df_tipo = self.recupera_tipo_codigo(id_tipo_quarto)

            # Remove o tipo de quarto da tabela
            self.mongo.db["tipo_quarto"].delete_one({"id_tipo_quarto": id_tipo_quarto})

            # Cria um novo objeto tipo_quarto para exibir os dados excluídos
            tipo_excluido = tipo_quarto(
                df_tipo.id_tipo_quarto.values[0],
                df_tipo.nome_tipo.values[0],
                df_tipo.descricao_tipo.values[0],
                df_tipo.capacidade_maxima.values[0],
                df_tipo.preco_diaria.values[0]
            )

            # Exibe os atributos excluídos
            print("Tipo de Quarto Removido com Sucesso!")
            print(tipo_excluido.to_string())
            self.mongo.close()
        else:
            self.mongo.close()
            print(f"O tipo de quarto ID {id_tipo_quarto} não existe.")

    def verifica_existencia_tipo_quarto(self, codigo:int=None, external: bool = False) -> bool:
        if external:
            # Cria uma nova conexão com o banco que permite alteração
            self.mongo.connect()

        # Recupera os dados do tipo de quarto criado transformando em um DataFrame
        df_tipo = pd.DataFrame(
            self.mongo.db["tipo_quarto"].find(
                {"id_tipo_quarto": codigo},
                {"id_tipo_quarto": 1, "_id": 0}
            )
        )

        if external:
            # Fecha a conexão com o Mongo
            self.mongo.close()

        return df_tipo.empty

    def recupera_tipo(self, _id:ObjectId=None) -> pd.DataFrame:
        # Recupera os dados do tipo de quarto criado transformando em um DataFrame
        df_tipo = pd.DataFrame(
            list(
                self.mongo.db["tipo_quarto"].find(
                    {"_id": _id},
                    {
                        "id_tipo_quarto": 1,
                        "nome_tipo": 1,
                        "descricao_tipo": 1,
                        "capacidade_maxima": 1,
                        "preco_diaria": 1,
                        "_id": 0
                    }
                )
            )
        )
        return df_tipo

    def recupera_tipo_codigo(self, codigo:int=None, external: bool = False) -> pd.DataFrame:
        if external:
            # Cria uma nova conexão com o banco que permite alteração
            self.mongo.connect()

        # Recupera os dados do tipo de quarto criado transformando em um DataFrame
        df_tipo = pd.DataFrame(
            list(
                self.mongo.db["tipo_quarto"].find(
                    {"id_tipo_quarto": codigo},
                    {
                        "id_tipo_quarto": 1,
                        "nome_tipo": 1,
                        "descricao_tipo": 1,
                        "capacidade_maxima": 1,
                        "preco_diaria": 1,
                        "_id": 0
                    }
                )
            )
        )

        if external:
            # Fecha a conexão com o Mongo
            self.mongo.close()

        return df_tipo
