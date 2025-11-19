# ARCHIVO PRINCIPAL DE LA APLICACIÓN

# en este archivo se creará el menú principal de la aplicación 
# y se llamarán a las funciones de gestión de cursos y estudiantes.

# Importar funciones de crud_operations.py
from crud_operations import insertar_curso, consultar_cursos, actualizar_curso
from database import get_conexion

# TAREA: Crear las funcion para gestionar estudiantes
# def gestionar_estudiantes():

# Función para gestionar profesores
def gestionar_cursos():
    while True:
        menu_curso="""
        \n---- Gestión de Cursos ----
        \n1. Insertar Curso
        \n2. Consultar Curso
        \n3. Actualizar Curso
        \n4. Eliminar Curso
        \n5. Volver al Menú Principal
        """
        
        print(menu_curso)
        
        opcion=input("Seleccione una Opción: ")
        
        if opcion=="1":
            id_curso = int(input("ID Curso: "))
            nombre = input("Nombre: ")
            cupos = int(input("Cupos: "))
            
            insertar_curso(id_curso, nombre, cupos)
        # TAREA: Crear las funciones para consultar, actualizar y eliminar libros
        elif opcion=="2":
            consultar_cursos()

        elif opcion=="3":
            id_curso = int(input("Ingrese el ID del curso a actualizar: "))
            print("Ingrese los nuevos datos del curso:")

            nombre = input("Nombre: ")
            cupos = int(input("Cupos: "))

            # Aquí llamamos la función de actualizar
            actualizar_curso(id_curso, nombre, cupos)
        
        elif opcion=="4":
           print("Eliminar curso no implementado")
           # TAREA: implementar eliminación de curso

        else:
            break
        
# Función que crea las tablas
# ----- Crear tablas en base de datos -----
def crear_tablas():
  TABLA_CURSO = '''
      CREATE TABLE IF NOT EXISTS CURSO (
          id_curso INT PRIMARY KEY,
          nombre VARCHAR(35),
          cupos INT
      )
  '''
  TABLA_ESTUDIANTE = '''
      CREATE TABLE IF NOT EXISTS ESTUDIANTE (
          rut VARCHAR(12) PRIMARY KEY,
          nombre VARCHAR(35),
          curso_id INT REFERENCES curso(id_curso)
      )
  '''

  conexion = get_conexion()
  if conexion:
    try:
      cursor = conexion.cursor()
      cursor.execute(TABLA_CURSO)
      cursor.execute(TABLA_ESTUDIANTE)
      conexion.commit() 
      print("=> Tablas creadas exitosamente")
    except Exception as e:
      print("Error al crear tablas: ", e)
    finally:
      cursor.close()
      conexion.close()

# Función para mostrar el menú principal
def main_menu():
    # Al iniciar la aplicación, crea las tablas:
    crear_tablas()

    while True:
        menu_principal="""
        \n---- Menú Principal ----
        \n1. Gestionar Cursos
        \n2. Gestionar Estudiantes
        \n3. Salir
        """
    
        print(menu_principal)
            
        opcion = input("Seleccione una Opción: ")
            
        if opcion == "1":
            gestionar_cursos()
        elif opcion=="2":
            print("Gestion de estudiantes no implementada.")
            # TAREA: Agregar funcion de gestion de estudiantes
        elif opcion=="3":
            print("Saliendo de la aplicación...")
            break
        else:
            print("Opción no válida, intente nuevamente")

# Ejecutar la función main_menu()
if __name__ == "__main__":
    main_menu()           
