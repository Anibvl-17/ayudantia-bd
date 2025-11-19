# ARCHIVO PARA REALIZAR OPERACIONES CRUD EN LA BASE DE DATOS

# Importar funcion de conexión a la base de datos
from database import get_conexion

# CRUD cursos
# Función para insertar un curso en la base de datos
def insertar_curso(id_curso, nombre, cupos):
    conexion = get_conexion()
    if conexion:
        try:
            cursor = conexion.cursor()
            query = "INSERT INTO CURSO (id_curso, nombre, cupos) VALUES (%s, %s, %s)"
            cursor.execute(query, (id_curso, nombre, cupos))
            conexion.commit() 
            print("El Curso ha sido agregado exitosamente a la BD")
        except Exception as e:
            print("Error al insertar el Curso: ", e)
        finally:
            cursor.close()
            conexion.close()

# Función para consultar los cursos en la base de datos
def consultar_cursos():
    conexion = get_conexion()
    if conexion:
        try:
            cursor = conexion.cursor()
            query = "SELECT * FROM CURSO"
            cursor.execute(query)
            cursos = cursor.fetchall()
            print("\n---- Lista de Cursos ----")
            for curso in cursos:
                print(f"ID: {curso[0]}, Nombre: {curso[1]}, Cupos: {curso[2]}")
        except Exception as e:
            print("Error al consultar los cursos: ", e)
        finally:
            cursor.close()
            conexion.close()
        
# Función para actualizar los cursos en la base de datos
def actualizar_curso(id_curso, nombre, cupos):
    conexion = get_conexion()
    if conexion:
        try:
            cursor = conexion.cursor()
            query = """
                UPDATE CURSO 
                SET nombre = %s, cupos = %s 
                WHERE id_curso = %s
            """
            cursor.execute(query, (nombre, cupos, id_curso))
            conexion.commit()
            if cursor.rowcount > 0:
                print("Curso actualizado exitosamente.")
            else:
                print("No se encontró un Curso con ese ID.")
        except Exception as e:
            print("Error al actualizar el Curso: ", e)
        finally:
            cursor.close()
            conexion.close()

# TAREA: Crear funcion para eliminar curso (verificar existencia!)
# def eliminar_curso(id_curso):

# --- CRUD estudiantes ---

# TAREA: Crear las funciones CRUD para estudiantes:
# - Insertar estudiante
# - Consultar estudiantes
# - Actualizar estudiante
# - Eliminar estudiante