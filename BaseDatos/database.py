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


def main():
    try:
        conexion = connect_to_database()
        insertar_perfil("perfil1", "usuario1", "contrasena1", "./Recursos/images/perfil1.png", "./Recursos/images/perfil1.png")
        profiles = obtener_perfiles_de_usuario()
        print("Perfiles de usuario cargados:", profiles)
        recuperar_imagen_perfil(conexion, "perfil1")
    except Error as e:
        print(f"Error en el programa: {e}")
    finally:
        if conexion:
            conexion.close()
            print("Conexión cerrada.")

if __name__ == "__main__":
    main()



