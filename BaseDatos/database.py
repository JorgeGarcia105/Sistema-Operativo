import mysql.connector
from mysql.connector import Error
from PIL import Image
import io

def connect_to_database():
    try:
        # Conectar a la base de datos
        conexion = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Jorge1002671250',
            database='perfiles_usuarios'
        )
        return conexion
    except mysql.connector.Error as err:
        print(f"Error al conectar a la base de datos: {err}")
        raise

def conectar_db(host, usuario, contraseña, nombre_db):
    try:
        conexion = mysql.connector.connect(
            host=host,
            user=usuario,
            password=contraseña,
            database=nombre_db
        )
        return conexion
    except mysql.connector.Error as err:
        print(f"Error al conectar a la base de datos: {err}")
        return None

def insertar_usuario(conexion, nombre, imagen, nombre_usuario, contrasena, imagen_fondo):
    try:
        cursor = conexion.cursor()
        sql = "INSERT INTO perfiles (nombre, imagen, nombre_usuario, contrasena, imagen_fondo) VALUES (%s, %s, %s, %s, %s)"
        val = (nombre, imagen, nombre_usuario, contrasena, imagen_fondo)
        cursor.execute(sql, val)
        conexion.commit()
        print("Usuario insertado correctamente.")
    except mysql.connector.Error as err:
        print(f"Error al insertar usuario: {err}")

def cerrar_conexion(conexion):
    conexion.close()
    print("Conexión cerrada.")

def close_connection(conexion):
    # Cerrar la conexión a la base de datos
    if conexion:
        conexion.close()

def  ejecutar_consulta(conexion, sql, params=None):
    try:
        cursor = conexion.cursor()
        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)
        return cursor
    except mysql.connector.Error as err:
        print(f"Error al ejecutar la consulta SQL: {err}")
        raise

def insertar_perfil(nombre, nombre_usuario, contrasena, imagen_path, imagen_fondo_path):
    conexion = connect_to_database()
    try:
        cursor = conexion.cursor()
        sql = "INSERT INTO perfiles (nombre, nombre_usuario, contrasena, imagen, imagen_fondo) VALUES (%s, %s, %s, %s, %s)"
        valores = (nombre, nombre_usuario, contrasena, imagen_path, imagen_fondo_path)  # Guarda la ruta de la imagen en la base de datos
        cursor.execute(sql, valores)
        conexion.commit()
    except mysql.connector.Error as err:
        print(f"Error al insertar en la base de datos: {err}")
    finally:
        close_connection(conexion)


def recuperar_imagen_perfil(conexion, nombre):
    try:
        cursor = conexion.cursor()
        sql = "SELECT imagen FROM perfiles WHERE nombre = %s"
        cursor.execute(sql, (nombre,))
        result = cursor.fetchone()
        if result:
            image_data = result[0]
            image = Image.open(io.BytesIO(image_data))
            image.show()
        else:
            print("Perfil no encontrado.")
    except Error as e:
        print(f"Error al recuperar imagen de perfil: {e}")


def obtener_perfiles_de_usuario():
    try:
        conexion = connect_to_database()
        cursor = conexion.cursor()
        sql = "SELECT nombre, imagen, nombre_usuario, contrasena FROM perfiles"
        cursor.execute(sql)
        profiles = {}
        for (nombre, imagen, nombre_usuario, contrasena) in cursor: # type: ignore
            profiles[nombre] = {
                'image': imagen,  # Asegúrate de que la imagen se almacena como datos binarios
                'username': nombre_usuario,
                'password': contrasena
            }
        cursor.close()
        conexion.close()
        return profiles
    except mysql.connector.Error as err:
        print(f"Error al obtener los perfiles de usuario: {err}")
        return None
    
def insertar_archivo_usuario(conexion, perfil_id, nombre_archivo, tipo_archivo):
    try:
        cursor = conexion.cursor()
        sql = "INSERT INTO archivos_usuario (perfil_id, nombre_archivo, tipo_archivo) VALUES (%s, %s, %s)"
        valores = (perfil_id, nombre_archivo, tipo_archivo)
        cursor.execute(sql, valores)
        conexion.commit()
        print("Archivo insertado correctamente.")
    except mysql.connector.Error as err:
        print(f"Error al insertar archivo: {err}")

def obtener_archivos_por_perfil(conexion, perfil_id):
    try:
        cursor = conexion.cursor()
        sql = "SELECT nombre_archivo, tipo_archivo FROM archivos_usuario WHERE perfil_id = %s"
        cursor.execute(sql, (perfil_id,))
        archivos = []
        for (nombre_archivo, tipo_archivo) in cursor:
            archivos.append({'nombre': nombre_archivo, 'tipo': tipo_archivo})
        return archivos
    except mysql.connector.Error as err:
        print(f"Error al obtener archivos del perfil: {err}")
        return []

def mostrar_archivos_por_perfil(conexion, perfil_id):
    archivos = obtener_archivos_por_perfil(conexion, perfil_id)
    if archivos:
        print(f"Archivos del perfil {perfil_id}:")
        for archivo in archivos:
            print(f"Nombre: {archivo['nombre']}, Tipo: {archivo['tipo']}")
    else:
        print("No se encontraron archivos para este perfil.")

def main():
    try:
        conexion = connect_to_database()
        
        # Insertar un perfil de ejemplo
        insertar_perfil("perfil1", "usuario1", "contrasena1", "./Recursos/images/perfil1.png", "./Recursos/images/perfil1.png")

        # Obtener el ID del perfil insertado
        cursor = conexion.cursor()
        cursor.execute("SELECT id FROM perfiles WHERE nombre = 'perfil1'")
        perfil_id = cursor.fetchone()[0] # type: ignore

        # Insertar archivos asociados al perfil
        insertar_archivo_usuario(conexion, perfil_id, "archivo1.txt", "Texto")
        insertar_archivo_usuario(conexion, perfil_id, "archivo2.jpg", "Imagen")
        insertar_archivo_usuario(conexion, perfil_id, "archivo3.mp4", "Video")

        # Mostrar los archivos asociados al perfil
        mostrar_archivos_por_perfil(conexion, perfil_id)
    except Error as e:
        print(f"Error en el programa: {e}")
    finally:
        if conexion:
            conexion.close()
            print("Conexión cerrada.")


if __name__ == "__main__":
    main()

