#fichier qu'on peut utiliser pour tester la connexion de Python à la base de données PostgreSQL
from sqlalchemy import text
from backend.database import engine

try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT version()"))
        print("Connexion PostgreSQL réussie !")
        print(result.scalar())
except Exception as exc:
    print("Échec de la connexion PostgreSQL.")
    print(f"Erreur : {exc}")
