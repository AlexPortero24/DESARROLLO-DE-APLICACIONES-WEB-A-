from conexion.conexion import get_connection

conexion = get_connection()

if conexion:
    print("¡Conexión exitosa con MySQL!")
    conexion.close()
else:
    print("No se pudo conectar con MySQL.")