from model.Reserva import Reserva
from model.Hospede import Hospede
from model.Quarto import Quarto
from conexion.mongodb_queries import MongoDBConnection
import decimal
from datetime import datetime

class Controller_Reserva:
    def __init__(self):
        self.mongo = MongoDBConnection()
    
    def verifica_existencia_hospede_quarto(self, cpf_hospede: str, numero_quarto: str):
        # Busca Hóspede por CPF
        hospede = self.mongo.db["hospede"].find_one({"documento": cpf_hospede})
        if not hospede:
            print(f"ERRO: Hóspede com CPF {cpf_hospede} não encontrado.")
            return None, None

        # Busca Quarto por Número
        quarto = self.mongo.db["quarto"].find_one({"numero_quarto": numero_quarto})
        if not quarto:
            print(f"ERRO: Quarto com número {numero_quarto} não encontrado.")
            return None, None

        return hospede, quarto # Retorna os objetos completos (dicionários)

    def inserir_reserva(self) -> Reserva:
        self.mongo.connect()
        
        print("\n--- INSERÇÃO DE NOVA RESERVA ---")
        cpf_hospede = input("CPF do Hóspede: ")
        numero_quarto = input("Número do Quarto: ")
        
        # Validação de FKs (Hospede e Quarto)
        hospede_dict, quarto_dict = self.verifica_existencia_hospede_quarto(cpf_hospede, numero_quarto)
        
        if hospede_dict is None or quarto_dict is None:
             self.mongo.close()
             return None

        data_checkin = input("Data de Check-in (AAAA-MM-DD): ")
        data_checkout = input("Data de Check-out (AAAA-MM-DD): ")
        valor_total = float(input("Valor Total: "))
        quant_hospedes = int(input("Quantidade de Hóspedes: "))
        status = input("Status da Reserva (EX: CONFIRMADA): ")

        proximo_id = self.recupera_proximo_id()
        
        # Cria o documento
        data = dict(
            id_reserva=proximo_id,
            id_hospede=hospede_dict["id_hospede"],
            id_quarto=quarto_dict["id_quarto"],
            data_checkin=data_checkin, # Pode converter para datetime se quiser
            data_checkout=data_checkout,
            quant_hospedes=quant_hospedes,
            status=status,
            valor_total=valor_total,
            data_reserva=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )

        self.mongo.db["reserva"].insert_one(data)
        self.mongo.close()

        # Cria objetos para compor a Reserva (POO)
        obj_hospede = Hospede(hospede_dict["id_hospede"], hospede_dict["documento"], hospede_dict["nome"], hospede_dict["sobrenome"])
        obj_quarto = Quarto(quarto_dict["id_quarto"], quarto_dict["numero_quarto"])

        nova_reserva = Reserva(
            proximo_id,
            obj_hospede,
            obj_quarto,
            data_checkin,
            data_checkout,
            data['data_reserva'],
            decimal.Decimal(valor_total),
            quant_hospedes,
            status
        )
        
        print(nova_reserva.to_string())
        return nova_reserva

    def atualizar_reserva(self) -> Reserva:
        self.mongo.connect()
        id_reserva = int(input("Código da Reserva que irá alterar: "))

        if self.verifica_existencia_reserva(id_reserva):
            novo_valor = float(input("Novo Valor Total: "))

            self.mongo.db["reserva"].update_one(
                {"id_reserva": id_reserva},
                {"$set": {"valor_total": novo_valor}}
            )
            
            reserva_dict = self.mongo.db["reserva"].find_one({"id_reserva": id_reserva})
            self.mongo.close()
            
            # Para reconstruir o objeto completo, precisaria buscar hospede/quarto novamente
            # Simplificando para retorno básico com IDs
            print(f"Reserva {id_reserva} atualizada com sucesso para valor: {novo_valor}")
            return None 
        else:
            self.mongo.close()
            print(f"O código {id_reserva} não existe.")
            return None

    def excluir_reserva(self):
        self.mongo.connect()
        id_reserva = int(input("Código da Reserva que irá excluir: "))

        if self.verifica_existencia_reserva(id_reserva):
            self.mongo.db["reserva"].delete_one({"id_reserva": id_reserva})
            self.mongo.close()
            print("Reserva Removida com Sucesso!")
        else:
            self.mongo.close()
            print(f"O código {id_reserva} não existe.")

    def verifica_existencia_reserva(self, id_reserva:int=None) -> bool:
        return self.mongo.db["reserva"].find_one({"id_reserva": id_reserva}) is not None

    def recupera_proximo_id(self) -> int:
        ultimo = self.mongo.db["reserva"].find_one(sort=[("id_reserva", -1)])
        if ultimo:
            return ultimo["id_reserva"] + 1
        return 1
