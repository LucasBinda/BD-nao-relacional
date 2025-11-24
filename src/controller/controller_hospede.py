from model.Hospede import Hospede
from conexion.mongodb_queries import MongoDBConnection
import pandas as pd

class Controller_Hospede:
    def __init__(self):
        self.mongo = MongoDBConnection()

    def inserir_hospede(self) -> Hospede:
        self.mongo.connect()
        
        print("\n--- INSERÇÃO DE NOVO HÓSPEDE ---")
        documento = input("Documento/CPF (Novo): ")

        if not self.verifica_existencia_hospede(documento):
            
            nome = input("Nome: ")
            sobrenome = input("Sobrenome: ")
            email = input("Email: ")
            telefone = input("Telefone: ")
            
            # Gera o próximo ID (Simulando Sequence)
            proximo_id = self.recupera_proximo_id()

            hospede_doc = {
                "id_hospede": proximo_id,
                "documento": documento,
                "nome": nome,
                "sobrenome": sobrenome,
                "email": email,
                "telefone": telefone
            }

            self.mongo.db["hospede"].insert_one(hospede_doc)
            self.mongo.close()

            novo_hospede = Hospede(proximo_id, documento, nome, sobrenome, email, telefone)
            print(novo_hospede.to_string())
            return novo_hospede
        else:
            self.mongo.close()
            print(f"O Documento/CPF {documento} já está cadastrado.")
            return None

    def atualizar_hospede(self) -> Hospede:
        self.mongo.connect()
        documento = input("Documento/CPF do hóspede que deseja alterar: ")

        if self.verifica_existencia_hospede(documento):
            
            novo_nome = input("Nome (Novo): ")
            novo_sobrenome = input("Sobrenome (Novo): ")
            novo_email = input("Email (Novo): ")
            novo_telefone = input("Telefone (Novo): ")

            self.mongo.db["hospede"].update_one(
                {"documento": documento},
                {"$set": {
                    "nome": novo_nome,
                    "sobrenome": novo_sobrenome,
                    "email": novo_email,
                    "telefone": novo_telefone
                }}
            )
            
            # Recupera o ID para retornar o objeto completo
            hospede_atual = self.mongo.db["hospede"].find_one({"documento": documento})
            self.mongo.close()

            hospede_atualizado = Hospede(
                hospede_atual["id_hospede"], 
                documento, 
                novo_nome, 
                novo_sobrenome, 
                novo_email, 
                novo_telefone
            )
            print(hospede_atualizado.to_string())
            return hospede_atualizado
        else:
            self.mongo.close()
            print(f"O Documento/CPF {documento} não existe.")
            return None

    def excluir_hospede(self):
        self.mongo.connect()
        documento = input("Documento/CPF do Hóspede que irá excluir: ")

        if self.verifica_existencia_hospede(documento):
            
            # Recupera dados antes de excluir para exibir
            hospede_rec = self.mongo.db["hospede"].find_one({"documento": documento})
            
            self.mongo.db["hospede"].delete_one({"documento": documento})
            self.mongo.close()

            hospede_excluido = Hospede(
                hospede_rec["id_hospede"], 
                hospede_rec["documento"], 
                hospede_rec["nome"], 
                hospede_rec["sobrenome"], 
                hospede_rec["email"], 
                hospede_rec["telefone"]
            )
            print("Hóspede Removido com Sucesso!")
            print(hospede_excluido.to_string())
        else:
            self.mongo.close()
            print(f"O Documento/CPF {documento} não existe.")

    def verifica_existencia_hospede(self, documento:str=None) -> bool:
        # Método auxiliar para verificar se o documento existe
        resultado = self.mongo.db["hospede"].find_one({"documento": documento})
        return resultado is not None

    def recupera_proximo_id(self) -> int:
        # Método auxiliar para gerar ID sequencial
        ultimo = self.mongo.db["hospede"].find_one(sort=[("id_hospede", -1)])
        if ultimo:
            return ultimo["id_hospede"] + 1
        return 1
