import mysql.connector
from mysql.connector import Error
from tkinter import Tk, Label, Entry, Button, messagebox, filedialog, Listbox, END
import os
import shutil

# Ruta base donde se almacenarán los archivos
RUTA_BASE = r"C:\Users\garci\OneDrive\Desktop\Uni\7 semestre\Sistemas Operativos\SistemaOperativo\Recursos\usuarios"

# Conectar a la base de datos
def connect_to_database():
    try:
        conexion = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Jorge1002671250',
            database='perfiles_usuarios'
        )
        return conexion
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al conectar a la base de datos: {err}")
        raise

# Autenticar usuario
def autenticar_usuario(conexion, nombre_usuario, contrasena):
    try:
        cursor = conexion.cursor()
        sql = "SELECT id, nombre FROM usuarios WHERE nombre_usuario = %s AND contrasena = %s"
        cursor.execute(sql, (nombre_usuario, contrasena))
        resultado = cursor.fetchone()
        if resultado:
            return {'id': resultado[0], 'nombre': resultado[1]}
        else:
            return None
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al autenticar usuario: {err}")
        return None

# Insertar archivo asociado a un perfil
def insertar_archivo_usuario(conexion, carpeta_id, nombre_archivo, file_path):
    try:
        cursor = conexion.cursor()
        # Obtener el nombre de la carpeta del usuario según el id de la carpeta
        nombre_carpeta_usuario = obtener_nombre_carpeta_usuario(conexion, carpeta_id)
        if nombre_carpeta_usuario:
            ruta_carpeta_usuario = os.path.join(RUTA_BASE, nombre_carpeta_usuario)
            if not os.path.exists(ruta_carpeta_usuario):
                os.makedirs(ruta_carpeta_usuario)
            
            # Determinar la subcarpeta según el tipo de archivo (ejemplo)
            tipo_archivo = os.path.splitext(file_path)[1].lower()
            if tipo_archivo in ('.mp3', '.wav', '.flac'):
                subcarpeta = 'musica'
            elif tipo_archivo in ('.mp4', '.avi', '.mkv'):
                subcarpeta = 'videos'
            elif tipo_archivo in ('.doc', '.docx', '.pdf'):
                subcarpeta = 'documentos'
            else:
                subcarpeta = 'otros'
            
            # Ruta completa de la subcarpeta
            ruta_subcarpeta = os.path.join(ruta_carpeta_usuario, subcarpeta)
            if not os.path.exists(ruta_subcarpeta):
                os.makedirs(ruta_subcarpeta)
            
            # Copiar el archivo a la subcarpeta correspondiente
            shutil.copy(file_path, os.path.join(ruta_subcarpeta, nombre_archivo))

            # Insertar el registro en la base de datos
            sql = "INSERT INTO archivos (nombre_archivo, ruta_archivo, carpeta_id) VALUES (%s, %s, %s)"
            valores = (nombre_archivo, os.path.join(subcarpeta, nombre_archivo), carpeta_id)
            cursor.execute(sql, valores)
            conexion.commit()
            messagebox.showinfo("Éxito", "Archivo insertado correctamente.")
        else:
            messagebox.showerror("Error", "No se encontró la carpeta del usuario.")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al insertar archivo: {err}")
    except Exception as e:
        messagebox.showerror("Error", f"Error al copiar archivo localmente: {str(e)}")

# Obtener el nombre de la carpeta del usuario según el id de la carpeta
def obtener_nombre_carpeta_usuario(conexion, carpeta_id):
    try:
        cursor = conexion.cursor()
        sql = "SELECT nombre FROM carpetas WHERE id = %s"
        cursor.execute(sql, (carpeta_id,))
        resultado = cursor.fetchone()
        if resultado:
            return resultado[0]
        else:
            return None
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al obtener nombre de la carpeta del usuario: {err}")
        return None

# Obtener archivos por carpeta del usuario y tipo de archivo
def obtener_archivos_por_carpeta(conexion, carpeta_id):
    try:
        cursor = conexion.cursor()
        sql = "SELECT nombre_archivo, ruta_archivo FROM archivos WHERE carpeta_id = %s"
        cursor.execute(sql, (carpeta_id,))
        archivos = []
        for (nombre_archivo, ruta_archivo) in cursor:
            archivos.append({'nombre': nombre_archivo, 'file_path': ruta_archivo})
        return archivos
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al obtener archivos del perfil: {err}")
        return []

def eliminar_archivo_usuario(conexion, archivo_id):
    try:
        cursor = conexion.cursor()

        # Obtener ruta del archivo antes de eliminarlo
        sql_select = "SELECT ruta_archivo FROM archivos WHERE id = %s"
        cursor.execute(sql_select, (archivo_id,))
        resultado = cursor.fetchone()
        if resultado:
            ruta_archivo = resultado[0]

            # Eliminar el archivo de la base de datos
            sql_delete = "DELETE FROM archivos WHERE id = %s"
            cursor.execute(sql_delete, (archivo_id,))
            conexion.commit()

            # Eliminar el archivo localmente
            if os.path.exists(ruta_archivo):
                os.remove(ruta_archivo)
                messagebox.showinfo("Éxito", "Archivo eliminado correctamente.")
            else:
                messagebox.showerror("Error", "No se encontró el archivo localmente.")
        else:
            messagebox.showerror("Error", "No se encontró el archivo en la base de datos.")

    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al eliminar archivo: {err}")
    except Exception as e:
        messagebox.showerror("Error", f"Error al eliminar archivo localmente: {str(e)}")

# Mostrar archivos por carpeta del usuario
def mostrar_archivos_por_carpeta(listbox, archivos):
    listbox.delete(0, END)
    if archivos:
        for archivo in archivos:
            listbox.insert(END, f"Nombre: {archivo['nombre']}, Ruta: {archivo['file_path']}")
    else:
        listbox.insert(END, "No se encontraron archivos para esta carpeta.")

# Obtener carpetas por usuario
def obtener_carpetas_usuario(usuario_id):
    try:
        conexion = connect_to_database()
        cursor = conexion.cursor()
        sql = "SELECT id, nombre FROM carpetas WHERE usuario_id = %s"
        cursor.execute(sql, (usuario_id,))
        carpetas = []
        for (id_carpeta, nombre_carpeta) in cursor:
            carpetas.append({'id': id_carpeta, 'nombre': nombre_carpeta})
        return carpetas
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al obtener carpetas del usuario: {err}")
        return []
    finally:
        if conexion:
            conexion.close()

# Mostrar carpetas del usuario
def mostrar_carpetas(listbox, carpetas):
    listbox.delete(0, END)
    if carpetas:
        for carpeta in carpetas:
            listbox.insert(END, f"{carpeta['nombre']}")
    else:
        listbox.insert(END, "No se encontraron carpetas para este usuario.")
class Aplicacion:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.conexion = self.connect_to_database()
        self.root = Tk()
        self.root.title("Sistema de Archivos")

        # Interfaz gráfica: etiquetas, campos de entrada y botón de login
        self.label_usuario = Label(self.root, text="Usuario")
        self.label_usuario.pack()
        self.entry_usuario = Entry(self.root)
        self.entry_usuario.pack()

        self.label_contrasena = Label(self.root, text="Contraseña")
        self.label_contrasena.pack()
        self.entry_contrasena = Entry(self.root, show="*")
        self.entry_contrasena.pack()

        self.boton_login = Button(self.root, text="Login", command=self.login)
        self.boton_login.pack()

        # Listbox para mostrar carpetas y archivos
        self.carpetas_listbox = Listbox(self.root, width=100)
        self.carpetas_listbox.pack()

        self.archivos_listbox = Listbox(self.root, width=100)
        self.archivos_listbox.pack()

        # Botones para acciones de la aplicación
        self.boton_mostrar_carpetas = Button(self.root, text="Mostrar mis carpetas", command=self.mostrar_carpetas)
        self.boton_mostrar_carpetas.pack()

        self.boton_mostrar_archivos = Button(self.root, text="Mostrar archivos de carpeta", command=self.mostrar_archivos)
        self.boton_mostrar_archivos.pack()

        self.boton_subir_archivo = Button(self.root, text="Subir archivo", command=self.subir_archivo)
        self.boton_subir_archivo.pack()

        self.boton_eliminar_archivo = Button(self.root, text="Eliminar archivo", command=self.eliminar_archivo)
        self.boton_eliminar_archivo.pack()

        self.usuario = None

    def connect_to_database(self):
        try:
            conexion = mysql.connector.connect(
                host='localhost',
                user=self.username,
                password=self.password,
                database='perfiles_usuarios'
            )
            return conexion
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al conectar a la base de datos: {err}")
            raise

    def login(self):
        nombre_usuario = self.entry_usuario.get()
        contrasena = self.entry_contrasena.get()
        self.usuario = self.autenticar_usuario(nombre_usuario, contrasena)
        if self.usuario:
            messagebox.showinfo("Éxito", f"Bienvenido, {self.usuario['nombre']}")
            self.mostrar_carpetas()
        else:
            messagebox.showerror("Error", "Nombre de usuario o contraseña incorrectos.")

    def autenticar_usuario(self, nombre_usuario, contrasena):
        try:
            cursor = self.conexion.cursor()
            sql = "SELECT id, nombre FROM usuarios WHERE nombre_usuario = %s AND contrasena = %s"
            cursor.execute(sql, (nombre_usuario, contrasena))
            resultado = cursor.fetchone()
            if resultado:
                return {'id': resultado[0], 'nombre': resultado[1]}
            else:
                return None
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al autenticar usuario: {err}")
            return None

    def mostrar_carpetas(self):
        if self.usuario:
            carpetas = self.obtener_carpetas_usuario(self.usuario['id'])
            self.mostrar_carpetas_en_lista(carpetas)
        else:
            messagebox.showerror("Error", "Debe iniciar sesión primero.")

    def mostrar_carpetas_en_lista(self, carpetas):
        self.carpetas_listbox.delete(0, END)
        if carpetas:
            for carpeta in carpetas:
                self.carpetas_listbox.insert(END, f"{carpeta['nombre']}")
        else:
            self.carpetas_listbox.insert(END, "No se encontraron carpetas para este usuario.")

    def obtener_carpetas_usuario(self, usuario_id):
        try:
            cursor = self.conexion.cursor()
            sql = "SELECT id, nombre FROM carpetas WHERE usuario_id = %s"
            cursor.execute(sql, (usuario_id,))
            carpetas = [{'id': id_carpeta, 'nombre': nombre_carpeta} for (id_carpeta, nombre_carpeta) in cursor]
            return carpetas
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al obtener carpetas del usuario: {err}")
            return []
        finally:
            if cursor:
                cursor.close()

    def mostrar_archivos(self):
        if self.usuario:
            seleccionado = self.carpetas_listbox.curselection()
            if seleccionado:
                indice = seleccionado[0]
                carpeta_seleccionada = self.carpetas_listbox.get(indice)
                carpeta_id = self.obtener_id_carpeta_por_nombre(self.usuario['id'], carpeta_seleccionada)
                if carpeta_id:
                    archivos = self.obtener_archivos_por_carpeta(carpeta_id)
                    self.mostrar_archivos_en_lista(archivos)
                else:
                    messagebox.showerror("Error", "No se encontró la carpeta del usuario.")
        else:
            messagebox.showerror("Error", "Debe iniciar sesión primero.")

    def obtener_id_carpeta_por_nombre(self, usuario_id, nombre_carpeta):
        try:
            cursor = self.conexion.cursor()
            sql = "SELECT id FROM carpetas WHERE usuario_id = %s AND nombre = %s"
            cursor.execute(sql, (usuario_id, nombre_carpeta))
            resultado = cursor.fetchone()
            if resultado:
                return resultado[0]
            else:
                return None
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al obtener ID de la carpeta: {err}")
            return None

    def obtener_archivos_por_carpeta(self, carpeta_id):
        try:
            cursor = self.conexion.cursor()
            sql = "SELECT nombre_archivo, ruta_archivo FROM archivos WHERE carpeta_id = %s"
            cursor.execute(sql, (carpeta_id,))
            archivos = [{'nombre': nombre_archivo, 'ruta': ruta_archivo} for (nombre_archivo, ruta_archivo) in cursor]
            return archivos
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al obtener archivos del perfil: {err}")
            return []
        finally:
            if cursor:
                cursor.close()

    def mostrar_archivos_en_lista(self, archivos):
        self.archivos_listbox.delete(0, END)
        if archivos:
            for archivo in archivos:
                self.archivos_listbox.insert(END, f"Nombre: {archivo['nombre']}, Ruta: {archivo['ruta']}")
        else:
            self.archivos_listbox.insert(END, "No se encontraron archivos para esta carpeta.")

    def subir_archivo(self):
        if self.usuario:
            file_path = filedialog.askopenfilename()
            if file_path:
                nombre_archivo = os.path.basename(file_path)
                carpeta_seleccionada = self.carpetas_listbox.get(self.carpetas_listbox.curselection()[0])
                carpeta_id = self.obtener_id_carpeta_por_nombre(self.usuario['id'], carpeta_seleccionada)
                if carpeta_id:
                    self.insertar_archivo_usuario(carpeta_id, nombre_archivo, file_path)
                    self.mostrar_archivos()  # Actualizar la lista de archivos después de subir
                else:
                    messagebox.showerror("Error", "No se encontró la carpeta del usuario.")
        else:
            messagebox.showerror("Error", "Debe iniciar sesión primero.")

    def insertar_archivo_usuario(self, carpeta_id, nombre_archivo, file_path):
        try:
            cursor = self.conexion.cursor()
            # Obtener el nombre de la carpeta del usuario según el id de la carpeta
            nombre_carpeta_usuario = self.obtener_nombre_carpeta_usuario(carpeta_id)
            if nombre_carpeta_usuario:
                ruta_carpeta_usuario = os.path.join(RUTA_BASE, nombre_carpeta_usuario)
                if not os.path.exists(ruta_carpeta_usuario):
                    os.makedirs(ruta_carpeta_usuario)
                
                # Determinar la subcarpeta según el tipo de archivo (ejemplo)
                tipo_archivo = os.path.splitext(file_path)[1].lower()
                if tipo_archivo in ('.mp3', '.wav', '.flac'):
                    subcarpeta = 'musica'
                elif tipo_archivo in ('.mp4', '.avi', '.mkv'):
                    subcarpeta = 'videos'
                elif tipo_archivo in ('.doc', '.docx', '.pdf'):
                    subcarpeta = 'documentos'
                else:
                    subcarpeta = 'otros'
                
                               # Ruta completa de la subcarpeta
                ruta_subcarpeta = os.path.join(ruta_carpeta_usuario, subcarpeta)
                if not os.path.exists(ruta_subcarpeta):
                    os.makedirs(ruta_subcarpeta)
                
                # Copiar el archivo a la subcarpeta correspondiente
                shutil.copy(file_path, os.path.join(ruta_subcarpeta, nombre_archivo))

                # Insertar el registro en la base de datos
                sql = "INSERT INTO archivos (nombre_archivo, ruta_archivo, carpeta_id) VALUES (%s, %s, %s)"
                valores = (nombre_archivo, os.path.join(subcarpeta, nombre_archivo), carpeta_id)
                cursor.execute(sql, valores)
                self.conexion.commit()
                messagebox.showinfo("Éxito", "Archivo insertado correctamente.")
            else:
                messagebox.showerror("Error", "No se encontró la carpeta del usuario.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al insertar archivo: {err}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al copiar archivo localmente: {str(e)}")

    def obtener_nombre_carpeta_usuario(self, carpeta_id):
        try:
            cursor = self.conexion.cursor()
            sql = "SELECT nombre FROM carpetas WHERE id = %s"
            cursor.execute(sql, (carpeta_id,))
            resultado = cursor.fetchone()
            if resultado:
                return resultado[0]
            else:
                return None
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al obtener nombre de la carpeta del usuario: {err}")
            return None

    def eliminar_archivo(self):
        if self.usuario:
            seleccionado = self.archivos_listbox.curselection()
            if seleccionado:
                indice = seleccionado[0]
                archivo_seleccionado = self.archivos_listbox.get(indice)
                archivo_nombre = archivo_seleccionado.split(",")[0].split(":")[1].strip()
                archivo_ruta = archivo_seleccionado.split(",")[1].split(":")[1].strip()
                archivo_id = self.obtener_id_archivo_por_nombre(archivo_nombre, archivo_ruta)
                if archivo_id:
                    self.eliminar_archivo_usuario(archivo_id)
                    self.mostrar_archivos()  # Actualizar la lista de archivos después de eliminar
                else:
                    messagebox.showerror("Error", "No se encontró el archivo seleccionado.")
        else:
            messagebox.showerror("Error", "Debe iniciar sesión primero.")

    def obtener_id_archivo_por_nombre(self, nombre_archivo, ruta_archivo):
        try:
            cursor = self.conexion.cursor()
            sql = "SELECT id FROM archivos WHERE nombre_archivo = %s AND ruta_archivo = %s"
            cursor.execute(sql, (nombre_archivo, ruta_archivo))
            resultado = cursor.fetchone()
            if resultado:
                return resultado[0]
            else:
                return None
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al obtener ID del archivo: {err}")
            return None

    def eliminar_archivo_usuario(self, archivo_id):
        try:
            cursor = self.conexion.cursor()

            # Obtener ruta del archivo antes de eliminarlo
            sql_select = "SELECT ruta_archivo FROM archivos WHERE id = %s"
            cursor.execute(sql_select, (archivo_id,))
            resultado = cursor.fetchone()
            if resultado:
                ruta_archivo = resultado[0]

                # Eliminar el archivo de la base de datos
                sql_delete = "DELETE FROM archivos WHERE id = %s"
                cursor.execute(sql_delete, (archivo_id,))
                self.conexion.commit()

                # Eliminar el archivo localmente
                if os.path.exists(ruta_archivo):
                    os.remove(ruta_archivo)
                    messagebox.showinfo("Éxito", "Archivo eliminado correctamente.")
                else:
                    messagebox.showerror("Error", "No se encontró el archivo localmente.")
            else:
                messagebox.showerror("Error", "No se encontró el archivo en la base de datos.")

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al eliminar archivo: {err}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar archivo localmente: {str(e)}")

    def run(self):
        self.root.mainloop()

# Ejecutar la aplicación
if __name__ == "__main__":
    # Asumiendo que el nombre de usuario y contraseña se proporcionan al iniciar la aplicación
    username = "root"  # Reemplazar con tu nombre de usuario de MySQL
    password = "Jorge1002671250"  # Reemplazar con tu contraseña de MySQL

    app = Aplicacion(username, password)
    app.run()

