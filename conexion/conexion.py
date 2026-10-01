import os
import psycopg2
from psycopg2.extras import RealDictCursor


def get_connection():
    try:
        database_url = os.getenv("DATABASE_URL")

        if database_url:
            conexion = psycopg2.connect(
                database_url,
                cursor_factory=RealDictCursor
            )
        else:
            conexion = psycopg2.connect(
                host="localhost",
                user="postgres",
                password=os.getenv("POSTGRES_PASSWORD"),
                database="acuario_vaporeon",
                port="5432",
                cursor_factory=RealDictCursor
            )

        return conexion

    except Exception as e:
        print(f"Error al conectar con PostgreSQL: {e}")
        return None