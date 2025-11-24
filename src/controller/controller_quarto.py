from model.Quarto import Quarto
from model.tipo_quarto import tipo_quarto
from conexion.mongodb_queries import MongoDBConnection

class Controller_Quarto:
    def __init__(self):
        self.mongo = MongoDBConnection()

    def inserir_quarto(self) -> Quarto:
        self.mongo.connect()
        
        print("\n--- INSERÇÃO DE NOVO QUARTO ---")
        numero_quarto = input("Número do Quarto (Novo): ")
        andar_quarto = int(input("Andar do Quarto (Novo): "))
        id_tipo_quarto = int(input("ID do Tipo de Quarto: "))
        status = input("Status do Quarto (Novo): ")

        # Validação de FK (Tipo Quarto)
        tipo_existente = self.mongo.db["tipo_quarto"].find_one({"id_tipo_quarto": id_tipo_quarto})
        
        if not tipo_existente:
            self.mongo.close()
            print(f"ERRO: O Tipo de Quarto ID {id_tipo_quarto} não existe.")
            return None

        proximo_id = self.recupera_proximo_id()

        data = dict(
            id_quarto=proximo_id,
            numero_quarto=numero_quarto,
            andar_quarto=andar_quarto,
            id_tipo_quarto=id_tipo_quarto,
            status=status
        )

        self.mongo.db["quarto"].insert_one(data)
        self.mongo.close()

        # Cria objeto Tipo para compor o Quarto
        obj_tipo = tipo_quarto(tipo_existente["id_tipo_quarto"], tipo_existente["nome_tipo"])
        
        novo_quarto = Quarto(proximo_id, numero_quarto, andar_quarto, obj_tipo, status)
        print(novo_quarto.to_string())
        return novo_quarto

    def atualizar_quarto(self) -> Quarto:
        self.mongo.connect()
        id_quarto = int(input("ID do Quarto que irá alterar: "))

        if self.verifica_existencia_quarto(id_quarto):
            numero_quarto = input("Número do Quarto (Novo): ")
            andar_quarto = int(input("Andar (Novo): "))
            id_tipo_quarto = int(input("ID do Tipo de Quarto (Novo): "))
            status = input("Status (Novo): ")
            
            # Valida novo tipo
            tipo_existente = self.mongo.db["tipo_quarto"].find_one({"id_tipo_quarto": id_tipo_quarto})
            if not tipo_existente:
                self.mongo.close()
                print(f"ERRO: O Tipo de Quarto ID {id_tipo_quarto} não existe.")
                return None

            self.mongo.db["quarto"].update_one(
                {"id_quarto": id_quarto},
                {"$set": {
                    "numero_quarto": numero_quarto,
                    "andar_quarto": andar_quarto,
                    "id_tipo_quarto": id_tipo_quarto,
                    "status": status
                }}
            )
            self.mongo.close()
            
            obj_tipo = tipo_quarto(tipo_existente["id_tipo_quarto"], tipo_existente["nome_tipo"])
            quarto_atualizado = Quarto(id_quarto, numero_quarto, andar_quarto, obj_tipo, status)
            print(quarto_atualizado.to_string())
            return quarto_atualizado
        else:
            self.mongo.close()
            print(f"O quarto ID {id_quarto} não existe.")
            return None

    def excluir_quarto(self):
        self.mongo.connect()
        id_quarto = int(input("ID do Quarto que irá excluir: "))

        if self.verifica_existencia_quarto(id_quarto):
            dados = self.mongo.db["quarto"].find_one({"id_quarto": id_quarto})
            # Recupera tipo para exibir
            tipo_dados = self.mongo.db["tipo_quarto"].find_one({"id_tipo_quarto": dados["id_tipo_quarto"]})
            
            self.mongo.db["quarto"].delete_one({"id_quarto": id_quarto})
            self.mongo.close()

            obj_tipo = tipo_quarto(tipo_dados["id_tipo_quarto"], tipo_dados["nome_tipo"])
            quarto_excluido = Quarto(dados["id_quarto"], dados["numero_quarto"], dados["andar_quarto"], obj_tipo, dados["status"])
            
            print("Quarto Removido com Sucesso!")
            print(quarto_excluido.to_string())
        else:
            self.mongo.close()
            print(f"O quarto ID {id_quarto} não existe.")

    def verifica_existencia_quarto(self, id_quarto:int=None) -> bool:
        return self.mongo.db["quarto"].find_one({"id_quarto": id_quarto}) is not None

    def recupera_proximo_id(self) -> int:
        ultimo = self.mongo.db["quarto"].find_one(sort=[("id_quarto", -1)])
        if ultimo:
            return ultimo["id_quarto"] + 1
        return 1
