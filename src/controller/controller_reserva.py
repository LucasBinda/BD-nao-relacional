import pandas as pd
from model.Reserva import Reserva
from conexion.mongo_queries import MongoQueries
from datetime import datetime

class Controller_Reserva:
    def __init__(self):
        self.mongo = MongoQueries()

    def inserir_reserva(self) -> Reserva:
        # Cria uma nova conexão com o banco que permite alteração
        self.mongo.connect()

        # Solicita ao usuario o novo ID da Reserva (gerado manualmente)
        id_reserva = input("ID da Reserva (Novo): ")

        if self.verifica_existencia_reserva(id_reserva):
            # Solicita ao usuario os dados necessários da reserva
            id_hospede = input("ID do Hóspede: ")
            id_quarto = input("ID do Quarto: ")
            data_checkin = input("Data Check-in (AAAA-MM-DD): ")
            data_checkout = input("Data Check-out (AAAA-MM-DD): ")
            quant_hospedes = input("Quantidade de Hóspedes: ")
            status = input("Status da Reserva: ")
            valor_total = input("Valor Total: ")
            data_reserva = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Insere e persiste a nova reserva
            self.mongo.db["reserva"].insert_one({
                "id_reserva": id_reserva,
                "id_hospede": id_hospede,
                "id_quarto": id_quarto,
                "data_checkin": data_checkin,
                "data_checkout": data_checkout,
                "quant_hospedes": quant_hospedes,
                "status": status,
                "valor_total": valor_total,
                "data_reserva": data_reserva
            })

            # Recupera os dados da nova reserva criada transformando em um DataFrame
            df_reserva = self.recupera_reserva(id_reserva)

            # Cria um novo objeto reserva
            nova_reserva = Reserva(
                df_reserva.id_reserva.values[0],
                df_reserva.id_hospede.values[0],
                df_reserva.id_quarto.values[0],
                df_reserva.data_checkin.values[0],
                df_reserva.data_checkout.values[0],
                df_reserva.data_reserva.values[0],
                df_reserva.valor_total.values[0],
                df_reserva.quant_hospedes.values[0],
                df_reserva.status.values[0]
            )

            # Exibe os atributos da nova reserva
            print(nova_reserva.to_string())
            self.mongo.close()

            # Retorna o objeto nova_reserva para utilização posterior, caso necessário
            return nova_reserva

        else:
            self.mongo.close()
            print(f"O ID da Reserva {id_reserva} já está cadastrado.")
            return None

    def atualizar_reserva(self) -> Reserva:
        # Cria uma nova conexão com o banco que permite alteração
        self.mongo.connect()

        # Solicita ao usuário o código da reserva a ser alterada
        id_reserva = input("ID da Reserva que deseja atualizar: ")

        # Verifica se a reserva existe na base de dados
        if not self.verifica_existencia_reserva(id_reserva):
            # Solicita ao usuario o novo valor total
            novo_valor_total = input("Novo Valor Total: ")

            # Atualiza o valor total da reserva existente
            self.mongo.db["reserva"].update_one(
                {"id_reserva": f"{id_reserva}"},
                {"$set": {"valor_total": novo_valor_total}}
            )

            # Recupera os dados da reserva atualizada transformando em um DataFrame
            df_reserva = self.recupera_reserva(id_reserva)

            # Cria um novo objeto reserva
            reserva_atualizada = Reserva(
                df_reserva.id_reserva.values[0],
                df_reserva.id_hospede.values[0],
                df_reserva.id_quarto.values[0],
                df_reserva.data_checkin.values[0],
                df_reserva.data_checkout.values[0],
                df_reserva.data_reserva.values[0],
                df_reserva.valor_total.values[0],
                df_reserva.quant_hospedes.values[0],
                df_reserva.status.values[0]
            )

            # Exibe os atributos da reserva atualizada
            print(reserva_atualizada.to_string())
            self.mongo.close()

            # Retorna o objeto reserva_atualizada para utilização posterior, caso necessário
            return reserva_atualizada
        else:
            self.mongo.close()
            print(f"O ID da Reserva {id_reserva} não existe.")
            return None

    def excluir_reserva(self):
        # Cria uma nova conexão com o banco que permite alteração
        self.mongo.connect()

        # Solicita ao usuário o ID da reserva a ser alterada
        id_reserva = input("ID da Reserva que irá excluir: ")

        # Verifica se a reserva existe na base de dados
        if not self.verifica_existencia_reserva(id_reserva):
            # Recupera os dados da reserva transformando em um DataFrame
            df_reserva = self.recupera_reserva(id_reserva)

            # Remove a reserva da tabela
            self.mongo.db["reserva"].delete_one({"id_reserva": f"{id_reserva}"})

            # Cria um novo objeto reserva para informar que foi removida
            reserva_excluida = Reserva(
                df_reserva.id_reserva.values[0],
                df_reserva.id_hospede.values[0],
                df_reserva.id_quarto.values[0],
                df_reserva.data_checkin.values[0],
                df_reserva.data_checkout.values[0],
                df_reserva.data_reserva.values[0],
                df_reserva.valor_total.values[0],
                df_reserva.quant_hospedes.values[0],
                df_reserva.status.values[0]
            )

            self.mongo.close()
            # Exibe os atributos da reserva excluída
            print("Reserva Removida com Sucesso!")
            print(reserva_excluida.to_string())
        else:
            self.mongo.close()
            print(f"O ID da Reserva {id_reserva} não existe.")

    def verifica_existencia_reserva(self, id_reserva:str=None, external:bool=False) -> bool:
        if external:
            # Cria uma nova conexão com o banco que permite alteração
            self.mongo.connect()

        # Recupera os dados da reserva transformando em um DataFrame
        df_reserva = pd.DataFrame(
            self.mongo.db["reserva"].find(
                {"id_reserva": f"{id_reserva}"},
                {
                    "id_reserva": 1,
                    "id_hospede": 1,
                    "id_quarto": 1,
                    "data_checkin": 1,
                    "data_checkout": 1,
                    "quant_hospedes": 1,
                    "status": 1,
                    "valor_total": 1,
                    "data_reserva": 1,
                    "_id": 0
                }
            )
        )

        if external:
            # Fecha a conexão com o Mongo
            self.mongo.close()

        return df_reserva.empty

    def recupera_reserva(self, id_reserva:str=None, external:bool=False) -> pd.DataFrame:
        if external:
            # Cria uma nova conexão com o banco que permite alteração
            self.mongo.connect()

        # Recupera os dados da reserva transformando em um DataFrame
        df_reserva = pd.DataFrame(
            list(
                self.mongo.db["reserva"].find(
                    {"id_reserva": f"{id_reserva}"},
                    {
                        "id_reserva": 1,
                        "id_hospede": 1,
                        "id_quarto": 1,
                        "data_checkin": 1,
                        "data_checkout": 1,
                        "quant_hospedes": 1,
                        "status": 1,
                        "valor_total": 1,
                        "data_reserva": 1,
                        "_id": 0
                    }
                )
            )
        )

        if external:
            # Fecha a conexão com o Mongo
            self.mongo.close()

        return df_reserva
