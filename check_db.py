from sqlalchemy import text
from backend.database import engine

with engine.connect() as connection:
    print("Base utilisée :", connection.execute(
        text("SELECT current_database()")
    ).scalar())

    print("Serveur :", connection.execute(
        text("SELECT inet_server_addr(), inet_server_port()")
    ).fetchone())

    for table in ["advisors", "customers", "users"]:
        count = connection.execute(
            text(f'SELECT COUNT(*) FROM "{table}"')
        ).scalar()
        print(f"{table}: {count}")