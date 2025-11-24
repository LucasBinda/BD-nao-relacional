from conexion.mongodb_queries import MongoDBConnection
from datetime import datetime

def seed_data():
    mongo = MongoDBConnection()
    mongo.connect()
    
    # 1. Limpar Coleções Antigas
    print("Limpando banco de dados...")
    colecoes = ["hospede", "tipo_quarto", "quarto", "reserva", "pagamento"]
    for col in colecoes:
        mongo.db[col].delete_many({})

    # 2. Inserir Hóspedes
    print("Inserindo Hóspedes...")
    hospedes = [
        {"id_hospede": 1, "nome": "JOÃO SILVA", "sobrenome": "SOUZA", "email": "joao@email.com", "telefone": "27999999999", "documento": "12345678900"},
        {"id_hospede": 2, "nome": "MARIA OLIVEIRA", "sobrenome": "SANTOS", "email": "maria@email.com", "telefone": "27988888888", "documento": "98765432100"},
        {"id_hospede": 3, "nome": "CARLOS PEREIRA", "sobrenome": "MACHADO", "email": "carlos@email.com", "telefone": "27977777777", "documento": "45678912300"},
    ]
    mongo.db["hospede"].insert_many(hospedes)

    # 3. Inserir Tipos de Quarto
    print("Inserindo Tipos de Quarto...")
    tipos = [
        {"id_tipo_quarto": 1, "nome_tipo": "STANDARD", "descricao_tipo": "Simples", "capacidade_maxima": 2, "preco_diaria": 150.0},
        {"id_tipo_quarto": 2, "nome_tipo": "LUXO", "descricao_tipo": "Vista Mar", "capacidade_maxima": 3, "preco_diaria": 350.0},
        {"id_tipo_quarto": 3, "nome_tipo": "MASTER", "descricao_tipo": "Hidro", "capacidade_maxima": 2, "preco_diaria": 600.0},
    ]
    mongo.db["tipo_quarto"].insert_many(tipos)

    # 4. Inserir Quartos
    print("Inserindo Quartos...")
    quartos = [
        {"id_quarto": 1, "numero_quarto": "101", "andar_quarto": 1, "id_tipo_quarto": 1, "status": "LIVRE"},
        {"id_quarto": 2, "numero_quarto": "102", "andar_quarto": 1, "id_tipo_quarto": 1, "status": "OCUPADO"},
        {"id_quarto": 3, "numero_quarto": "201", "andar_quarto": 2, "id_tipo_quarto": 2, "status": "LIVRE"},
    ]
    mongo.db["quarto"].insert_many(quartos)

    # 5. Inserir Reservas
    print("Inserindo Reservas...")
    reservas = [
        {
            "id_reserva": 1, "id_hospede": 1, "id_quarto": 2, 
            "data_checkin": "2025-10-20", "data_checkout": "2025-10-25", 
            "quant_hospedes": 2, "status": "CONFIRMADA", "valor_total": 750.0,
            "data_reserva": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    ]
    mongo.db["reserva"].insert_many(reservas)

    # 6. Inserir Pagamentos
    print("Inserindo Pagamentos...")
    pagamentos = [
        {
            "id_pagamento": 1, "id_reserva": 1, "valor": 750.0, 
            "data_pagamento": "2025-10-18", "metodo": "PIX", "status": "PAGO"
        }
    ]
    mongo.db["pagamento"].insert_many(pagamentos)

    mongo.close()
    print("Banco de dados MongoDB populado com sucesso!")

if __name__ == "__main__":
    seed_data()
