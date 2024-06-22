import tkinter as tk
from tkinter import messagebox
import psycopg2
import platform
from datetime import datetime

class Mi_Consola:
    def __init__(self, root):
        self.root = root
        self.root.title("Mi Consola de Música")
        self.root.geometry("400x600")  # Cambiar el tamaño de la ventana

        # Crear usuario
        self.frame_usuario = tk.Frame(root)
        self.frame_usuario.pack(pady=10)

        self.label_usuario = tk.Label(self.frame_usuario, text="Registrar Usuario")
        self.label_usuario.pack()

        self.entry_nombre_usuario = tk.Entry(self.frame_usuario)
        self.entry_nombre_usuario.pack()
        self.entry_nombre_usuario.insert(0, "Nombre")

        self.entry_contrasena_usuario = tk.Entry(self.frame_usuario)
        self.entry_contrasena_usuario.pack()
        self.entry_contrasena_usuario.insert(0, "Contraseña")

        self.entry_correo_usuario = tk.Entry(self.frame_usuario)
        self.entry_correo_usuario.pack()
        self.entry_correo_usuario.insert(0, "Correo")

        self.button_registrar_usuario = tk.Button(self.frame_usuario, text="Registrarse", command=self.registrar_usuario)
        self.button_registrar_usuario.pack(pady=5)

        self.frame_login = tk.Frame(root)
        self.frame_login.pack(pady=10)

        self.label_login = tk.Label(self.frame_login, text="Iniciar Sesión")
        self.label_login.pack()

        self.entry_correo_login = tk.Entry(self.frame_login)
        self.entry_correo_login.pack()
        self.entry_correo_login.insert(0, "Correo")

        self.entry_contrasena_login = tk.Entry(self.frame_login)
        self.entry_contrasena_login.pack()
        self.entry_contrasena_login.insert(0, "Contraseña")

        self.button_iniciar_sesion = tk.Button(self.frame_login, text="Iniciar Sesión", command=self.iniciar_sesion)
        self.button_iniciar_sesion.pack(pady=5)

    def conectar_db(self):
        # Conectar a la base de datos PostgreSQL
        conn = psycopg2.connect(
            dbname="Youtune",
            user="postgres",
            password="root",
            host="localhost",
            port="5432"
        )
        return conn

    def registrar_usuario(self):
        nombre = self.entry_nombre_usuario.get()
        contrasena = self.entry_contrasena_usuario.get()
        correo = self.entry_correo_usuario.get()
        dispositivos = platform.platform()  # Obtener información del dispositivo
        fecha_registro = datetime.now()  # Obtener la fecha y hora actual

        conn = self.conectar_db()
        cursor = conn.cursor()

        try:
            # Verificar si el correo ya existe
            cursor.execute('SELECT * FROM Usuario WHERE correo = %s', (correo,))
            if cursor.fetchone():
                messagebox.showerror("Error", "El correo ya está registrado")
            else:
                # Obtener el próximo id_usuario
                cursor.execute('SELECT COALESCE(MAX(id_usuario), 0) + 1 FROM Usuario')
                next_id = cursor.fetchone()[0]

                # Insertar nuevo usuario
                cursor.execute('''
                INSERT INTO Usuario (id_usuario, nombre, contrasena, correo, dispositivos, fecha_registro) 
                VALUES (%s, %s, %s, %s, %s, %s)
                ''', (next_id, nombre, contrasena, correo, dispositivos, fecha_registro))
                conn.commit()
                messagebox.showinfo("Éxito", f"Usuario {nombre} registrado con éxito")

        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar usuario: {e}")
        finally:
            cursor.close()
            conn.close()

    def iniciar_sesion(self):
        correo = self.entry_correo_login.get()
        contrasena = self.entry_contrasena_login.get()

        conn = self.conectar_db()
        cursor = conn.cursor()

        try:
            # Verificar las credenciales del usuario
            cursor.execute('SELECT * FROM Usuario WHERE correo = %s AND contrasena = %s', (correo, contrasena))
            usuario = cursor.fetchone()
            if usuario:
                messagebox.showinfo("Éxito", f"Bienvenido {usuario[1]}")
            else:
                messagebox.showerror("Error", "Correo o contraseña incorrectos")
        except Exception as e:
            messagebox.showerror("Error", f"Error al iniciar sesión: {e}")
        finally:
            cursor.close()
            conn.close()

# Ejemplo de uso
if __name__ == "__main__":
    root = tk.Tk()
    app = Mi_Consola(root)
    root.mainloop()
