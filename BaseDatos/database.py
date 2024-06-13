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
            valores = (nombre_archivo, os.path.join(nombre_carpeta_usuario, subcarpeta, nombre_archivo), carpeta_id)
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
def obtener_archivos_por_carpeta(conexion, carpeta_id, tipo_archivo):
    try:
        cursor = conexion.cursor()
        sql = "SELECT nombre_archivo, ruta_archivo FROM archivos WHERE carpeta_id = %s AND ruta_archivo LIKE %s"
        cursor.execute(sql, (carpeta_id, f"%/{tipo_archivo}/%"))
        archivos = []
        for (nombre_archivo, ruta_archivo) in cursor:
            archivos.append({'nombre': nombre_archivo, 'file_path': ruta_archivo})
        return archivos
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al obtener archivos del perfil: {err}")
        return []

# Eliminar archivo por carpeta del usuario y nombre de archivo
def eliminar_archivo_usuario(conexion, carpeta_id, nombre_archivo):
    try:
        cursor = conexion.cursor()
        sql = "DELETE FROM archivos WHERE carpeta_id = %s AND nombre_archivo = %s"
        cursor.execute(sql, (carpeta_id, nombre_archivo))
        conexion.commit()
        # Eliminar el archivo localmente también
        nombre_carpeta_usuario = obtener_nombre_carpeta_usuario(conexion, carpeta_id)
        if nombre_carpeta_usuario:
            ruta_archivo = os.path.join(RUTA_BASE, nombre_carpeta_usuario, nombre_archivo)
            if os.path.exists(ruta_archivo):
                os.remove(ruta_archivo)
                messagebox.showinfo("Éxito", "Archivo eliminado correctamente.")
            else:
                messagebox.showerror("Error", "No se encontró el archivo localmente.")
        else:
            messagebox.showerror("Error", "No se encontró la carpeta del usuario.")
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

# Ventana principal
class Aplicacion:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Archivos")

        self.label_usuario = Label(root, text="Usuario")
        self.label_usuario.pack()
        self.entry_usuario = Entry(root)
        self.entry_usuario.pack()

        self.label_contrasena = Label(root, text="Contraseña")
        self.label_contrasena.pack()
        self.entry_contrasena = Entry(root, show="*")
        self.entry_contrasena.pack()

        self.boton_login = Button(root, text="Login", command=self.login)
        self.boton_login.pack()

        self.archivos_listbox = Listbox(root, width=100)
        self.archivos_listbox.pack()

        self.boton_mostrar_archivos = Button(root, text="Mostrar mis archivos", command=self.mostrar_archivos)
        self.boton_mostrar_archivos.pack()

        self.boton_subir_archivo = Button(root, text="Subir archivo", command=self.subir_archivo)
        self.boton_subir_archivo.pack()

        self.boton_eliminar_archivo = Button(root, text="Eliminar archivo", command=self.eliminar_archivo)
        self.boton_eliminar_archivo.pack()

        self.usuario = None
        self.conexion = connect_to_database()

    def login(self):
        nombre_usuario = self.entry_usuario.get()
        contrasena = self.entry_contrasena.get()
        self.usuario = autenticar_usuario(self.conexion, nombre_usuario, contrasena)
        if self.usuario:
            messagebox.showinfo("Éxito", f"Bienvenido, {self.usuario['nombre']}")
        else:
            messagebox.showerror("Error", "Nombre de usuario o contraseña incorrectos.")

    def obtener_id_carpeta_usuario(self, usuario_id):
        try:
            cursor = self.conexion.cursor()
            sql = "SELECT id FROM carpetas WHERE usuario_id = %s"
            cursor.execute(sql, (usuario_id,))
            resultado = cursor.fetchone()
            if resultado:
                return resultado[0] # type: ignore
            else:
                messagebox.showerror("Error", "No se encontró la carpeta del usuario.")
                return None
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al obtener ID de la carpeta del usuario: {err}")
            return None

    def mostrar_archivos(self):
        if self.usuario:
            id_carpeta = self.obtener_id_carpeta_usuario(self.usuario['id'])
            if id_carpeta:
                archivos = obtener_archivos_por_carpeta(self.conexion, id_carpeta, '')
                mostrar_archivos_por_carpeta(self.archivos_listbox, archivos)
        else:
            messagebox.showerror("Error", "Debe iniciar sesión primero.")

    def subir_archivo(self):
        if self.usuario:
            file_path = filedialog.askopenfilename()
            if file_path:
                nombre_archivo = os.path.basename(file_path)
                insertar_archivo_usuario(self.conexion, self.usuario['id'], nombre_archivo, file_path)
                self.mostrar_archivos()
        else:
            messagebox.showerror("Error", "Debe iniciar sesión primero.")

    def eliminar_archivo(self):
        if self.usuario:
            seleccionado = self.archivos_listbox.curselection()
            if seleccionado:
                indice = seleccionado[0]
                nombre_archivo = self.archivos_listbox.get(indice).split(",")[0].split(": ")[1].strip()
                eliminar_archivo_usuario(self.conexion, self.usuario['id'], nombre_archivo)
                self.mostrar_archivos()
        else:
            messagebox.showerror("Error", "Debe iniciar sesión primero.")

    def __del__(self):
        if self.conexion:
            self.conexion.close()

# Ejecutar la aplicación
if __name__ == "__main__":
    root = Tk()
    app = Aplicacion(root)
    root.mainloop()

