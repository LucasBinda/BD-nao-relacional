from model.tipo_quarto import tipo_quarto
from conexion.mongodb_queries import MongoDBConnection
import decimal

class Controller_TipoQuarto:
    def __init__(self):
        self.mongo = MongoDBConnection()

    def inserir_tipo_quarto(self) -> tipo_quarto:
        self.mongo.connect()
        
        print("\n--- INSERÇÃO DE NOVO TIPO DE QUARTO ---")
        nome_tipo = input("Nome do Tipo de Quarto (Novo): ")
        descricao_tipo = input("Descrição (Nova): ")
        capacidade_maxima = int(input("Capacidade Máxima (Nova): "))
        preco_diaria = float(input("Preço da Diária (Novo): ")) # Mongo usa float/double

        proximo_id = self.recupera_proximo_id()

        data = dict(
            id_tipo_quarto=proximo_id,
            nome_tipo=nome_tipo,
            descricao_tipo=descricao_tipo,
            capacidade_maxima=capacidade_maxima,
            preco_diaria=preco_diaria
        )

        self.mongo.db["tipo_quarto"].insert_one(data)
        self.mongo.close()

        novo_tipo = tipo_quarto(proximo_id, nome_tipo, descricao_tipo, capacidade_maxima, decimal.Decimal(preco_diaria))
        print(novo_tipo.to_string())
        return novo_tipo

    def atualizar_tipo_quarto(self) -> tipo_quarto:
        self.mongo.connect()
        id_tipo_quarto = int(input("ID do Tipo de Quarto que irá alterar: "))

        if self.verifica_existencia_tipo_quarto(id_tipo_quarto):
            nome_tipo = input("Nome do Tipo de Quarto (Novo): ")
            descricao_tipo = input("Descrição (Nova): ")
            capacidade_maxima = int(input("Capacidade Máxima (Nova): "))
            preco_diaria = float(input("Preço da Diária (Novo): "))

            self.mongo.db["tipo_quarto"].update_one(
                {"id_tipo_quarto": id_tipo_quarto},
                {"$set": {
                    "nome_tipo": nome_tipo,
                    "descricao_tipo": descricao_tipo,
                    "capacidade_maxima": capacidade_maxima,
                    "preco_diaria": preco_diaria
                }}
            )
            self.mongo.close()
            
            tipo_atualizado = tipo_quarto(id_tipo_quarto, nome_tipo, descricao_tipo, capacidade_maxima, decimal.Decimal(preco_diaria))
            print(tipo_atualizado.to_string())
            return tipo_atualizado
        else:
            self.mongo.close()
            print(f"O tipo de quarto ID {id_tipo_quarto} não existe.")
            return None

    def excluir_tipo_quarto(self):
        self.mongo.connect()
        id_tipo_quarto = int(input("ID do Tipo de Quarto que irá excluir: "))

        if self.verifica_existencia_tipo_quarto(id_tipo_quarto):
            # Recupera dados para exibir
            dados = self.mongo.db["tipo_quarto"].find_one({"id_tipo_quarto": id_tipo_quarto})
            
            self.mongo.db["tipo_quarto"].delete_one({"id_tipo_quarto": id_tipo_quarto})
            self.mongo.close()
            
            tipo_excluido = tipo_quarto(dados["id_tipo_quarto"], dados["nome_tipo"], dados["descricao_tipo"], dados["capacidade_maxima"], decimal.Decimal(dados["preco_diaria"]))
            print("Tipo de Quarto Removido com Sucesso!")
            print(tipo_excluido.to_string())
        else:
            self.mongo.close()
            print(f"O tipo de quarto ID {id_tipo_quarto} não existe.")

    def verifica_existencia_tipo_quarto(self, id_tipo_quarto:int=None) -> bool:
        return self.mongo.db["tipo_quarto"].find_one({"id_tipo_quarto": id_tipo_quarto}) is not None
    
    def recupera_proximo_id(self) -> int:
        ultimo = self.mongo.db["tipo_quarto"].find_one(sort=[("id_tipo_quarto", -1)])
        if ultimo:
            return ultimo["id_tipo_quarto"] + 1
        return 1
