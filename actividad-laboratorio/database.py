# CONEXIÓN A LA BASE DE DATOS

# Importar librería psycopg2
import psycopg2

# Función para obtener la conexión a la base de datos
def get_conexion():
    try:
        conexion = psycopg2.connect(
            database='', # Indicar la base de datos a la que se conectará
            user='postgres', # Indicar el usuario de la base de datos
            password='', # Indicar la contraseña del usuario
            host='localhost',  # Indicar el host donde se encuentra la base de datos
            port='5432' # Indicar el puerto donde se encuentra la base de datos
        )
        return conexion
    except psycopg2.Error as error:
        print("Error al conectar a la base de datos: ", error)
        return None
    
        