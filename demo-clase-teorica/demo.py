import psycopg2

###
# Demostracion de mini aplicacion conectada a PostgreSQL mediante psycopg2
# Utiliza dos tablas, persona y casa. Representa a personas dueñas de una o varias casas.
# Se relacionan a traves del atributo id_persona
#
# Funcionalidades:
#  - Consultar personas
#  - Consultar casas
#  - Agregar personas
#  - Editar personas
#  - Eliminar personas
###

try:
  # Recordar cambiar los datos de conexion de acuerdo a su base de datos
  conexion = psycopg2.connect(
    database = "demo",
    user = "postgres",
    password = "ubb",
    host = "localhost",
    port = "5432"
  )
  cursor = conexion.cursor()
  print("=> Conexión establecida con la base de datos!")
except psycopg2.Error as error:
  print("Error al conectar con la base de datos:", error)

# ----- Crear tablas en base de datos -----

TABLA_PERSONA = '''
CREATE TABLE IF NOT EXISTS persona (
  id_persona INT PRIMARY KEY,
  nombre VARCHAR(35),
  edad INT
)
'''

TABLA_CASA = '''
CREATE TABLE IF NOT EXISTS casa (
  id_casa INT PRIMARY KEY,
  id_persona INT REFERENCES persona(id_persona),
  direccion VARCHAR(50)
)
'''

try:
  cursor.execute(TABLA_PERSONA)
  cursor.execute(TABLA_CASA)
  conexion.commit()
  print("=> Tablas creadas o reemplazadas exitosamente!")
except Exception as error:
  print("Error al crear tablas:", error)

# ----- Agregar personas -----

INSERT_PERSONA = 'INSERT INTO persona (id_persona, nombre, edad) VALUES (%s, %s, %s)'

try:
  cursor.execute("SELECT * FROM persona")
  if cursor.rowcount == 0: # rowcount sirve para contar los resultados obtenidos en la consulta
    cursor.execute(INSERT_PERSONA, (1, 'Martina', 30))
    cursor.execute(INSERT_PERSONA, (2, 'Cristian', 45))
    cursor.execute(INSERT_PERSONA, (3, 'Carlos', 22))
    conexion.commit()
    print("=> Personas agregadas exitosamente!")
  else:
    print("=> Ya hay personas ingresadas.")
except Exception as error:
  print("Error al agregar personas:", error)

# ----- Agregar casas -----

INSERT_CASA = 'INSERT INTO casa (id_casa, id_persona, direccion) VALUES (%s, %s, %s)'

try:
  cursor.execute("SELECT * FROM casa")
  if cursor.rowcount == 0:
    cursor.execute(INSERT_CASA, (1, 1, 'Calle 123'))
    cursor.execute(INSERT_CASA, (2, 2, 'Avenida 100'))
    cursor.execute(INSERT_CASA, (3, 3, 'Pasaje 5'))
    conexion.commit()
    print("=> Casas agregadas exitosamente!")
  else:
    print("=> Ya hay casas ingresadas.")
except Exception as error:
  print("Error al agregar casas:", error)

# ----- Funciones de menu, validacion y CRUD -----

def mostrarMenu():
  print("\n..:: Menu ::..")
  print("1. Consultar personas")
  print("2. Consultar casas")
  print("3. Agregar persona")
  print("4. Editar persona")
  print("5. Eliminar persona")
  print("6. Salir")

# Valida que se ingresen solo numeros
def inputInt(mensaje):
  while True:
    try:
      # int() se usa para transformar el input de string a número
      # Ejemplo: opcion = "4" -> 4
      # strip() elimina los espacios al inicio y al final de la entrada
      # Ejemplo: input = "   hola mundo  " -> "hola mundo"
      numero = int(input(mensaje).strip())
      return numero
    except:
      print("Error: debe ingresar un numero")

# Valida que se ingresen solo letras
def inputString(mensaje):
  while True:
    try:
      str = input(mensaje).strip()

      # isalpha() verifica que el String tenga al menos 1 caracter y que sean solo letras
      if not str.isalpha():
        print("Error: solo se permiten letras")
        continue

      return str
    except:
      print("Error: debe ingresar texto")

def consultarPersonas():
  try:
    cursor.execute("SELECT * FROM persona")
    listaPersonas = cursor.fetchall() # fetchall() obtiene todos las tuplas de la consulta
    
    print("\n--- Lista de personas ---")
    for persona in listaPersonas: # persona = (id_persona, nombre, edad)
      id = persona[0]
      nombre = persona[1]
      edad = persona[2]
      print(f'- Persona {id}. Nombre: {nombre}. Edad: {edad}')
  except Exception as error:
    print("=> Error al consultar personas:", error)

def consultarCasas():
  try:
    cursor.execute("SELECT * FROM casa")
    listaCasas = cursor.fetchall()
    
    print("\n--- Lista de casas ---")
    for casa in listaCasas: # casa = (id_casa, id_persona, edad)
      id_casa = casa[0]
      id_persona = casa[1]
      direccion = casa[2]
      print(f'- Casa {id_casa}. ID persona: {id_persona}. Direccion: {direccion}')
  except Exception as error:
    print("=> Error al consultar casas:", error)

def agregarPersona():
  print("\n..:: Agregar persona ::..")
  print("Ingrese los datos de la persona.")
  print("Para regresar, ingrese 0 en el campo ID")

  while True:
    id = inputInt("ID Persona > ")

    # Si se ingresa 0 en id, simplemente retorna
    if id == 0: return

    try:
      cursor.execute("SELECT * FROM persona WHERE id_persona = %s", (id,))
      if cursor.rowcount > 0:
        print("ID ya existe, intente code nuevo.")
        continue

      nombre = inputString("Nombre > ")
      edad = inputInt("Edad > ")

      cursor.execute(INSERT_PERSONA, (id, nombre, edad))
      conexion.commit()

      print("=> Persona agregada exitosamente!")
      return
    except Exception as error:
      print("Error al agregar persona:", error)
      return
    
def editarPersona():
  print("\n..:: Editar persona ::..")
  print("Ingrese ID de la persona a editar")
  print("Para regresar, ingrese 0")

  while True:
    id = inputInt("ID Persona > ")

    # Si se ingresa 0 en id, simplemente retorna
    if id == 0: return

    try:
      cursor.execute("SELECT * FROM persona WHERE id_persona = %s", (id,))
      if cursor.rowcount == 0:
        print(f"No existe persona con ID {id}, intente de nuevo.")
        continue

      nombre = inputString("Nombre > ")
      edad = inputInt("Edad > ")

      cursor.execute('UPDATE persona SET nombre = %s, edad = %s WHERE id_persona = %s', (nombre, edad, id))
      conexion.commit()
      
      print("=> Persona actualizada exitosamente!")
      return
    except Exception as error:
      print("Error al agregar persona:", error)
      return
    
def eliminarPersona():
  print("\n..:: Eliminar persona ::..")
  print("Ingrese ID de la persona a eliminar.")
  print("Advertencia! Solo se pueden eliminar personas que no estan asociadas a una casa")
  print("Para regresar, ingrese 0")

  while True:
    id = inputInt("ID Persona > ")

    # Si se ingresa 0 en id, simplemente retorna
    if id == 0: return

    try:
      cursor.execute("SELECT * FROM persona WHERE id_persona = %s", (id,))
      if cursor.rowcount == 0:
        print(f"No existe persona con id {id}, intente de nuevo.")
        continue
      
      cursor.execute("SELECT * FROM casa WHERE id_persona = %s", (id,))
      if not cursor.rowcount == 0:
        print("La persona tiene casa(s) asociada(s), intente de nuevo.")
        continue

      # Elimina la persona 
      cursor.execute('DELETE FROM persona WHERE id_persona = %s', (id,))
      conexion.commit()

      print("=> Persona eliminada exitosamente!")
      return
    except Exception as error:
      print("Error al agregar persona:", error)
      return


# ----- Ciclo para menu -----

opcion = 0 # Almacena la opcion ingresada, opcion 6 es para salir

while opcion != 6:
  mostrarMenu()
  opcion = inputInt("Ingrese una opcion > ")
  
  if opcion ==1:
    consultarPersonas()
  elif opcion == 2:
    consultarCasas()
  elif opcion == 3:
    agregarPersona()
  elif opcion == 4:
    editarPersona()
  elif opcion == 5:
    eliminarPersona()
  else:
    conexion.close()
    cursor.close()
    print("=> Conexion y cursor cerrados.")
    print("--- Fin del programa ---")
    exit(0) # Finaliza el programa de forma exitosa

  