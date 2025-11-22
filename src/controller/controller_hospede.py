import pandas as pd
from model.Hospede import Hospede
from conexion.mongo_queries import MongoQueries

class Controller_Hospede:
    def __init__(self):
        self.mongo = MongoQueries()

    def inserir_hospede(self) -> Hospede:
        # Cria uma nova conexão com o banco que permite alteração
        self.mongo.connect()

        # Solicita ao usuario o novo Documento/CPF
        documento = input("Documento/CPF (Novo): ")

        if self.verifica_existencia_hospede(documento):
            # Solicita ao usuario o novo nome
            nome = input("Nome (Novo): ")
            sobrenome = input("Sobrenome (Novo): ")
            email = input("Email (Novo): ")
            telefone = input("Telefone (Novo): ")

            # Insere e persiste o novo hóspede
            self.mongo.db["hospedes"].insert_one({
                "documento": documento,
                "nome": nome,
                "sobrenome": sobrenome,
                "email": email,
                "telefone": telefone
            })

            # Recupera os dados do novo hóspede criado transformando em um DataFrame
            df_hospede = self.recupera_hospede(documento)

            # Cria um novo objeto Hospede
            novo_hospede = Hospede(
                df_hospede.documento.values[0],
                df_hospede.nome.values[0],
                df_hospede.sobrenome.values[0],
                df_hospede.email.values[0],
                df_hospede.telefone.values[0]
            )

            # Exibe os atributos do novo hóspede
            print(novo_hospede.to_string())
            self.mongo.close()
            # Retorna o objeto novo_hospede para utilização posterior, caso necessário
            return novo_hospede
        else:
            self.mongo.close()
            print(f"O Documento/CPF {documento} já está cadastrado.")
            return None

    def atualizar_hospede(self) -> Hospede:
        # Cria uma nova conexão com o banco que permite alteração
        self.mongo.connect()

        # Solicita ao usuário o código do hóspede a ser alterado
        documento = input("Documento/CPF do hóspede que deseja alterar: ")

        # Verifica se o hóspede existe na base de dados
        if not self.verifica_existencia_hospede(documento):
            # Solicita a nova descrição do hóspede
            novo_nome = input("Nome (Novo): ")
            novo_sobrenome = input("Sobrenome (Novo): ")
            novo_email = input("Email (Novo): ")
            novo_telefone = input("Telefone (Novo): ")

            # Atualiza o hóspede existente
            self.mongo.db["hospedes"].update_one(
                {"documento": f"{documento}"},
                {"$set": {
                    "nome": novo_nome,
                    "sobrenome": novo_sobrenome,
                    "email": novo_email,
                    "telefone": novo_telefone
                }}
            )

            # Recupera os dados do novo hóspede criado transformando em um DataFrame
            df_hospede = self.recupera_hospede(documento)

            # Cria um novo objeto hospede
            hospede_atualizado = Hospede(
                df_hospede.documento.values[0],
                df_hospede.nome.values[0],
                df_hospede.sobrenome.values[0],
                df_hospede.email.values[0],
                df_hospede.telefone.values[0]
            )

            # Exibe os atributos do novo hóspede
            print(hospede_atualizado.to_string())
            self.mongo.close()
            # Retorna o objeto hospede_atualizado para utilização posterior, caso necessário
            return hospede_atualizado
        else:
            self.mongo.close()
            print(f"O Documento/CPF {documento} não existe.")
            return None

    def excluir_hospede(self):
        # Cria uma nova conexão com o banco que permite alteração
        self.mongo.connect()

        # Solicita ao usuário o Documento/CPF do Hóspede a ser alterado
        documento = input("Documento/CPF do Hóspede que irá excluir: ")

        # Verifica se o hóspede existe na base de dados
        if not self.verifica_existencia_hospede(documento):
            # Recupera os dados do novo hóspede criado transformando em um DataFrame
            df_hospede = self.recupera_hospede(documento)

            # Revome o hóspede da tabela
            self.mongo.db["hospedes"].delete_one({"documento":f"{documento}"})

            # Cria um novo objeto Hospede para informar que foi removido
            hospede_excluido = Hospede(
                df_hospede.documento.values[0],
                df_hospede.nome.values[0],
                df_hospede.sobrenome.values[0],
                df_hospede.email.values[0],
                df_hospede.telefone.values[0]
            )

            self.mongo.close()
            # Exibe os atributos do hóspede excluído
            print("Hóspede Removido com Sucesso!")
            print(hospede_excluido.to_string())
        else:
            self.mongo.close()
            print(f"O Documento/CPF {documento} não existe.")

    def verifica_existencia_hospede(self, documento:str=None, external:bool=False) -> bool:
        if external:
            # Cria uma nova conexão com o banco que permite alteração
            self.mongo.connect()

        # Recupera os dados do novo hóspede criado transformando em um DataFrame
        df_hospede = pd.DataFrame(
            self.mongo.db["hospedes"].find(
                {"documento":f"{documento}"},
                {"documento": 1, "_id": 0}
            )
        )

        if external:
            # Fecha a conexão com o Mongo
            self.mongo.close()

        return df_hospede.empty

    def recupera_hospede(self, documento:str=None, external:bool=False) -> pd.DataFrame:
        if external:
            # Cria uma nova conexão com o banco que permite alteração
            self.mongo.connect()

        # Recupera os dados do novo hóspede criado transformando em um DataFrame
        df_hospede = pd.DataFrame(
            list(self.mongo.db["hospedes"].find(
                {"documento":f"{documento}"},
                {"_id": 0}
            ))
        )

        if external:
            # Fecha a conexão com o Mongo
            self.mongo.close()

        return df_hospede
