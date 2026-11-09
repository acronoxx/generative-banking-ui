import os

# database.py exige DB_PASSWORD dès l'import. On met une valeur factice :
# le moteur SQLAlchemy est créé mais ne se connecte jamais pendant les tests.
os.environ.setdefault("DB_PASSWORD", "test")
