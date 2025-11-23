import time
import os

SYSTEM_NAME = "Sistema de Gestão de Reservas Hoteleiras"
DISCIPLINA = "Banco de Dados"
PROFESSOR = "Prof. Howard Roatti"
INTEGRANTES = [
    "Amon",
    "Anna Luiza",
    "Victoria",
    "Laiza",
    "Lucas",
    "Mycaely"
]

# nomes de coleções esperadas (ajuste se seu modelo usar outros nomes)
COLLECTIONS = {
    "hospedes": "hospede",
    "quartos": "quarto",
    "reservas": "reserva"
}

def try_mongo_count(uri=None, dbname=None):
    """Tenta conectar ao MongoDB e retornar dict com contagens, ou raises on failure."""
    try:
        from pymongo import MongoClient
    except Exception as e:
        raise RuntimeError("pymongo não disponível") from e

    # default URI / DB - o usuário pode definir via env vars MONGO_URI e MONGO_DB
    uri = uri or os.environ.get("MONGO_URI", "mongodb://localhost:27017")
    dbname = dbname or os.environ.get("MONGO_DB", "hoteldb")

    client = MongoClient(uri, serverSelectionTimeoutMS=3000)
    # Força seleção do servidor para detectar falha rápido
    client.server_info()
    db = client[dbname]

    counts = {}
    for k, coll_name in COLLECTIONS.items():
        try:
            counts[k] = db[coll_name].count_documents({})
        except Exception:
            counts[k] = None
    client.close()
    return counts

def try_oracle_count():
    """
    Fallback: usa a classe OracleQueries (existe no projeto) para obter contagens.
    A OracleQueries deve prover um método execute_query(sql) que retorne lista de dicts,
    ou algo similar. Se não existir, retornaremos None para cada contagem.
    """
    try:
        from conexion.oracle_queries import OracleQueries
        oq = OracleQueries()
        def safe_count(q):
            try:
                res = oq.execute_query(q)
                # tenta pegar primeiro valor de chave (assume {'TOTAL': n} ou similar)
                if isinstance(res, list) and len(res) > 0:
                    row = res[0]
                    # pega o primeiro valor numérico encontrado
                    for v in row.values():
                        if isinstance(v, (int, float)):
                            return int(v)
                return None
            except Exception:
                return None
        counts = {}
        counts["hospedes"] = safe_count("SELECT COUNT(1) AS total_hospedes FROM hospede")
        counts["quartos"]  = safe_count("SELECT COUNT(1) AS total_quartos FROM quarto")
        counts["reservas"] = safe_count("SELECT COUNT(1) AS total_reservas FROM reserva")
        return counts
    except Exception:
        return {"hospedes": None, "quartos": None, "reservas": None}

def format_count(v):
    if v is None:
        return "N/A"
    return str(v)

def show_splash(wait_seconds=2.5):
    """Exibe splash no console e aguarda `wait_seconds` (com barra de progresso minimal)."""
    # Tenta MongoDB primeiro
    counts = None
    try:
        counts = try_mongo_count()
        source = "MongoDB"
    except Exception:
        counts = try_oracle_count()
        source = "Oracle (fallback)" if any(v is not None for v in counts.values()) else "Nenhum (N/A)"

    # Monta texto
    border = "#" * 72
    print("\n" + border)
    print(f"#  {SYSTEM_NAME}".ljust(72) + "#")
    print("#" + " " * 70 + "#")
    print(f"#  Disciplina : {DISCIPLINA}".ljust(72) + "#")
    print(f"#  Professor  : {PROFESSOR}".ljust(72) + "#")
    print("#" + " " * 70 + "#")
    print("#  Integrantes:".ljust(72) + "#")
    for name in INTEGRANTES:
        print(f"#    - {name}".ljust(72) + "#")
    print("#" + " " * 70 + "#")
    print("#  Contagem de registros (fonte: {})".ljust(72) + "#".format(source))
    print(f"#    - Hóspedes : {format_count(counts.get('hospedes'))}".ljust(72) + "#")
    print(f"#    - Quartos  : {format_count(counts.get('quartos'))}".ljust(72) + "#")
    print(f"#    - Reservas : {format_count(counts.get('reservas'))}".ljust(72) + "#")
    print(border + "\n")

    steps = 20
    for i in range(steps + 1):
        pct = int((i / steps) * 100)
        bar = "#" * (i) + "-" * (steps - i)
        print(f"\rIniciando... [{bar}] {pct}% ", end="", flush=True)
        time.sleep(wait_seconds / steps)
    print("\n")  

if __name__ == "__main__":
    show_splash()
