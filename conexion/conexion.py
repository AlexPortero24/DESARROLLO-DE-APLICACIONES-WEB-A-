import os
import mysql.connector
from mysql.connector import Error


def get_connection():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password=os.getenv("MYSQL_PASSWORD"),
            database="acuario_vaporeon"
        )

        if conexion.is_connected():
            return conexion

    except Error as e:
        print(f"Error al conectar con MySQL: {e}")

    return None