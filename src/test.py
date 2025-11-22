from conexion.mongodb_queries import MongoDBConnection


def main():

    mongo = MongoDBConnection()
    db = mongo.connect()
    print("Conexão OK")
    mongo.close()



if __name__ == "__main__" :
    main()