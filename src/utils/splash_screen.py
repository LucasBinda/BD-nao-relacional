from conexion.mongodb_queries import MongoDBConnection

class SplashScreen:
    def __init__(self):
        self.created_by = """
       #        ANNA LUIZA
        #        LAISA
        #        LUCAS
        #        MIKAELLY
        #        VICTORIA
        """
        self.mongo = MongoDBConnection()

    def get_total_hospedes(self):
        self.mongo.connect()
        total = self.mongo.db["hospede"].count_documents({})
        self.mongo.close()
        return total

    def get_total_quartos(self):
        self.mongo.connect()
        total = self.mongo.db["quarto"].count_documents({})
        self.mongo.close()
        return total

    def get_total_reservas(self):
        self.mongo.connect()
        total = self.mongo.db["reserva"].count_documents({})
        self.mongo.close()
        return total

    def get_updated_screen(self):
        return f"""
        ########################################################
        #        SISTEMA DE CONTROLE DE RESERVAS E HÓSPEDES        
        #                                                         
        #  TOTAL DE REGISTROS:                                    
        #      1 - HÓSPEDES:        {str(self.get_total_hospedes()).rjust(5)}
        #      2 - QUARTOS:         {str(self.get_total_quartos()).rjust(5)}
        #      3 - RESERVAS:        {str(self.get_total_reservas()).rjust(5)}
        #     
        #
        #  CRIADO POR: {self.created_by}
        #
        #  RELATÓRIOS DISPONÍVEIS:
        #      - Ocupação dos quartos
        #      - Número de reservas por mês
        ########################################################
        """
