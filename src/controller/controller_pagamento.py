from model.Pagamento import Pagamento
from model.Reserva import Reserva
from conexion.mongodb_queries import MongoDBConnection
import decimal
from datetime import datetime

class Controller_Pagamento:
    def __init__(self):
        self.mongo = MongoDBConnection()

    def inserir_pagamento(self) -> Pagamento:
        self.mongo.connect()
        
        id_reserva = int(input("ID da Reserva: "))
        
        # Verifica se a reserva existe
        reserva_existente = self.mongo.db["reserva"].find_one({"id_reserva": id_reserva})
        if not reserva_existente:
            self.mongo.close()
            print(f"ERRO: Reserva {id_reserva} não encontrada.")
            return None

        valor_pago = float(input("Valor Pago: "))
        data_pagamento = input("Data do Pagamento (AAAA-MM-DD): ")
        metodo = input("Método de Pagamento: ")
        status = input("Status do Pagamento: ")

        proximo_id = self.recupera_proximo_id()

        data = dict(
            id_pagamento=proximo_id,
            id_reserva=id_reserva,
            valor_pago=valor_pago,
            data_pagamento=data_pagamento,
            metodo=metodo,
            status=status
        )

        self.mongo.db["pagamento"].insert_one(data)
        self.mongo.close()

        # Cria Objeto Reserva dummy apenas com ID para compor Pagamento
        obj_reserva = Reserva(id_reserva=id_reserva)

        novo_pagamento = Pagamento(
            proximo_id,
            obj_reserva,
            decimal.Decimal(valor_pago),
            data_pagamento,
            metodo,
            status
        )

        print(novo_pagamento.to_string())
        return novo_pagamento

    def atualizar_pagamento(self) -> Pagamento:
        self.mongo.connect()
        id_pagamento = int(input("ID do Pagamento que irá alterar: "))

        if self.verifica_existencia_pagamento(id_pagamento):
            valor_pago = float(input("Novo Valor Pago: "))
            metodo = input("Novo Método de Pagamento: ")
            status = input("Novo Status do Pagamento: ")

            self.mongo.db["pagamento"].update_one(
                {"id_pagamento": id_pagamento},
                {"$set": {
                    "valor_pago": valor_pago,
                    "metodo": metodo,
                    "status": status
                }}
            )
            self.mongo.close()
            print(f"Pagamento {id_pagamento} atualizado com sucesso.")
            return None
        else:
            self.mongo.close()
            print(f"O pagamento ID {id_pagamento} não existe.")
            return None

    def excluir_pagamento(self):
        self.mongo.connect()
        id_pagamento = int(input("ID do Pagamento que irá excluir: "))

        if self.verifica_existencia_pagamento(id_pagamento):
            self.mongo.db["pagamento"].delete_one({"id_pagamento": id_pagamento})
            self.mongo.close()
            print("Pagamento Removido com Sucesso!")
        else:
            self.mongo.close()
            print(f"O pagamento ID {id_pagamento} não existe.")

    def verifica_existencia_pagamento(self, id_pagamento: int = None) -> bool:
        return self.mongo.db["pagamento"].find_one({"id_pagamento": id_pagamento}) is not None

    def recupera_proximo_id(self) -> int:
        ultimo = self.mongo.db["pagamento"].find_one(sort=[("id_pagamento", -1)])
        if ultimo:
            return ultimo["id_pagamento"] + 1
        return 1
