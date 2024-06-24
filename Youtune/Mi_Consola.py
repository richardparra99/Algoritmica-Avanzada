import tkinter as tk
from tkinter import messagebox, Menu
from PIL import Image, ImageTk  # Importar PIL para manejar imágenes
import psycopg2
from datetime import datetime

class Mi_Consola:
    def __init__(self, root):
        self.root = root
        self.root.title("Mi Consola de Música")
        self.root.geometry("800x400")
        self.root.configure(bg="#f0f0f0")

        # Estilos comunes
        self.entry_bg = "#ecf0f1"
        self.label_fg = "#2c3e50"
        self.button_bg = "#2980b9"
        self.button_fg = "#ecf0f1"
        self.font = ("Helvetica", 12)

        # Contenedor principal
        self.main_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.main_frame.pack(expand=True, fill="both")

        self.crear_registro()

    def crear_registro(self):
        self.limpiar_frames()

        # Cargar imagen de fondo
        self.image = Image.open("C:/Users/Richard-P/Algoritmica-Avanzada/Imagenes/YOUTUNE.png")  # Cambia esto por la ruta a tu imagen
        self.image = self.image.resize((400, 400), Image.Resampling.LANCZOS)  # Redimensionar si es necesario
        self.bg_image = ImageTk.PhotoImage(self.image)

        # Contenedor izquierdo (Registro)
        self.left_frame = tk.Frame(self.main_frame, bg="#ffffff", bd=2, relief="solid")
        self.left_frame.place(relwidth=0.5, relheight=1.0)

        self.label_sign_up = tk.Label(self.left_frame, text="Sign Up", bg="#ffffff", fg=self.label_fg, font=("Helvetica", 18, "bold"))
        self.label_sign_up.pack(pady=20)

        self.entry_nombre_usuario = tk.Entry(self.left_frame, bg=self.entry_bg, font=self.font)
        self.entry_nombre_usuario.pack(pady=10, padx=20)
        self.entry_nombre_usuario.insert(0, "Name")

        self.entry_correo_usuario = tk.Entry(self.left_frame, bg=self.entry_bg, font=self.font)
        self.entry_correo_usuario.pack(pady=10, padx=20)
        self.entry_correo_usuario.insert(0, "E-mail")
        self.entry_correo_usuario.bind('<FocusIn>', self.clear_entry)
        self.entry_correo_usuario.bind('<FocusOut>', lambda event, field=self.entry_correo_usuario, default="E-mail": self.restore_entry(event, field, default))

        self.entry_contrasena_usuario = tk.Entry(self.left_frame, bg=self.entry_bg, font=self.font, show="*")
        self.entry_contrasena_usuario.pack(pady=10, padx=20)
        self.entry_contrasena_usuario.insert(0, "Password")
        self.entry_contrasena_usuario.bind('<FocusIn>', self.clear_entry)
        self.entry_contrasena_usuario.bind('<FocusOut>', lambda event, field=self.entry_contrasena_usuario, default="Password": self.restore_entry(event, field, default))

        self.var_mostrar_contrasena_registro = tk.BooleanVar()
        self.check_mostrar_contrasena_registro = tk.Checkbutton(self.left_frame, text="Mostrar contraseña", variable=self.var_mostrar_contrasena_registro, command=self.mostrar_ocultar_contrasena_registro, bg="#ffffff", fg=self.label_fg, font=self.font)
        self.check_mostrar_contrasena_registro.pack(pady=5)

        self.button_registrar_usuario = tk.Button(self.left_frame, text="Registrarse", command=self.registrar_usuario, bg=self.button_bg, fg=self.button_fg, font=self.font)
        self.button_registrar_usuario.pack(pady=10)

        self.button_login_prompt = tk.Button(self.left_frame, text="¿Ya tienes una cuenta? Inicia sesión", command=self.crear_login, bg="#ffffff", fg=self.label_fg, font=self.font, bd=0)
        self.button_login_prompt.pack(pady=10)

        # Contenedor derecho (Bienvenida) con imagen de fondo
        self.right_frame = tk.Frame(self.main_frame, bg="#3498db", bd=2, relief="solid")
        self.right_frame.place(relx=0.5, relwidth=0.5, relheight=1.0)

        self.canvas = tk.Canvas(self.right_frame, width=400, height=400)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")

        self.label_login = tk.Label(self.right_frame, text="Glad to see You!", bg="#3498db", fg="#ffffff", font=("Helvetica", 18, "bold"))
        self.label_login.pack(pady=20)

    def crear_login(self):
        self.limpiar_frames()

        # Cargar imagen de fondo
        self.image = Image.open("C:/Users/Richard-P/Algoritmica-Avanzada/Imagenes/YOUTUNE.png")  # Cambia esto por la ruta a tu imagen
        self.image = self.image.resize((400, 400), Image.Resampling.LANCZOS)  # Redimensionar si es necesario
        self.bg_image = ImageTk.PhotoImage(self.image)

        # Contenedor derecho (Iniciar sesión)
        self.right_frame = tk.Frame(self.main_frame, bg="#ffffff", bd=2, relief="solid")
        self.right_frame.place(relwidth=0.5, relheight=1.0)

        self.label_login = tk.Label(self.right_frame, text="Sign In", bg="#ffffff", fg=self.label_fg, font=("Helvetica", 18, "bold"))
        self.label_login.pack(pady=20)

        self.entry_correo_login = tk.Entry(self.right_frame, bg=self.entry_bg, font=self.font)
        self.entry_correo_login.pack(pady=10, padx=20)
        self.entry_correo_login.insert(0, "E-mail")
        self.entry_correo_login.bind('<FocusIn>', self.clear_entry)
        self.entry_correo_login.bind('<FocusOut>', lambda event, field=self.entry_correo_login, default="E-mail": self.restore_entry(event, field, default))

        self.entry_contrasena_login = tk.Entry(self.right_frame, bg=self.entry_bg, font=self.font, show="*")
        self.entry_contrasena_login.pack(pady=10, padx=20)
        self.entry_contrasena_login.insert(0, "Password")
        self.entry_contrasena_login.bind('<FocusIn>', self.clear_entry)
        self.entry_contrasena_login.bind('<FocusOut>', lambda event, field=self.entry_contrasena_login, default="Password": self.restore_entry(event, field, default))

        self.var_mostrar_contrasena_login = tk.BooleanVar()
        self.check_mostrar_contrasena_login = tk.Checkbutton(self.right_frame, text="Mostrar contraseña", variable=self.var_mostrar_contrasena_login, command=self.mostrar_ocultar_contrasena_login, bg="#ffffff", fg=self.label_fg, font=self.font)
        self.check_mostrar_contrasena_login.pack(pady=5)

        self.button_iniciar_sesion = tk.Button(self.right_frame, text="SIGN IN", command=self.iniciar_sesion, bg=self.button_bg, fg=self.button_fg, font=self.font)
        self.button_iniciar_sesion.pack(pady=20)

        self.button_register_prompt = tk.Button(self.right_frame, text="¿No tienes una cuenta? Regístrate", command=self.crear_registro, bg="#ffffff", fg=self.label_fg, font=self.font, bd=0)
        self.button_register_prompt.pack(pady=10)

        # Contenedor izquierdo (Bienvenida) con imagen de fondo
        self.left_frame = tk.Frame(self.main_frame, bg="#3498db", bd=2, relief="solid")
        self.left_frame.place(relx=0.5, relwidth=0.5, relheight=1.0)

        self.canvas = tk.Canvas(self.left_frame, width=400, height=400)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")

        self.label_welcome = tk.Label(self.left_frame, text="Welcome Back!", bg="#3498db", fg="#ffffff", font=("Helvetica", 18, "bold"))
        self.label_welcome.pack(pady=20)

    def limpiar_frames(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def mostrar_ocultar_contrasena_registro(self):
        if self.var_mostrar_contrasena_registro.get():
            self.entry_contrasena_usuario.config(show="")
        else:
            self.entry_contrasena_usuario.config(show="*")

    def mostrar_ocultar_contrasena_login(self):
        if self.var_mostrar_contrasena_login.get():
            self.entry_contrasena_login.config(show="")
        else:
            self.entry_contrasena_login.config(show="*")

    def conectar_db(self):
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
        correo = self.entry_correo_usuario.get()
        contrasena = self.entry_contrasena_usuario.get()
        fecha_registro = datetime.now()

        conn = self.conectar_db()
        cursor = conn.cursor()

        try:
            cursor.execute('INSERT INTO Usuario (nombre, correo, contrasena, fecha_registro) VALUES (%s, %s, %s, %s)', (nombre, correo, contrasena, fecha_registro))
            conn.commit()
            messagebox.showinfo("Éxito", "Usuario registrado exitosamente")
            self.crear_login()  # Mostrar pantalla de inicio de sesión después del registro
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
            cursor.execute('SELECT * FROM Usuario WHERE correo = %s AND contrasena = %s', (correo, contrasena))
            usuario = cursor.fetchone()
            if (usuario):
                messagebox.showinfo("Éxito", f"Bienvenido {usuario[1]}")
                self.mostrar_panel_canciones()  # Mostrar el panel de canciones
            else:
                messagebox.showerror("Error", "Correo o contraseña incorrectos")
        except Exception as e:
            messagebox.showerror("Error", f"Error al iniciar sesión: {e}")
        finally:
            cursor.close()
            conn.close()

    def mostrar_panel_canciones(self):
        self.limpiar_frames()

        self.frame_canciones = tk.Frame(self.main_frame, bg="#ffffff")
        self.frame_canciones.pack(expand=True, fill="both")

        # Menú
        self.menu_bar = Menu(self.root)
        self.root.config(menu=self.menu_bar)

        self.menu_playlist = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_command(label="Playlist", command=self.mostrar_playlist)

        self.menu_artistas = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_command(label="Artistas", command=self.mostrar_artistas)

        self.menu_albumes = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_command(label="Álbumes", command=self.mostrar_albumes)

        self.menu_genero = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_command(label="Género", command=self.mostrar_genero)

        self.label_canciones = tk.Label(self.frame_canciones, text="Todas las Canciones", bg="#ffffff", fg=self.label_fg, font=("Helvetica", 18, "bold"))
        self.label_canciones.pack(pady=20)

        self.entry_busqueda = tk.Entry(self.frame_canciones, bg=self.entry_bg, font=self.font)
        self.entry_busqueda.pack(pady=10, padx=20)
        self.entry_busqueda.insert(0, "Buscar canciones...")
        self.entry_busqueda.bind('<FocusIn>', self.clear_entry)
        self.entry_busqueda.bind('<FocusOut>', lambda event, field=self.entry_busqueda, default="Buscar canciones...": self.restore_entry(event, field, default))

        self.button_buscar = tk.Button(self.frame_canciones, text="Buscar", command=self.buscar_canciones, bg=self.button_bg, fg=self.button_fg, font=self.font)
        self.button_buscar.pack(pady=10)

        self.frame_lista_canciones = tk.Frame(self.frame_canciones, bg="#ffffff")
        self.frame_lista_canciones.pack(expand=True, fill="both", padx=20, pady=10)

        self.actualizar_lista_canciones()

    def actualizar_lista_canciones(self):
        for widget in self.frame_lista_canciones.winfo_children():
            widget.destroy()

        conn = self.conectar_db()
        cursor = conn.cursor()

        try:
            cursor.execute('SELECT * FROM Musica')
            canciones = cursor.fetchall()

            for cancion in canciones:
                label_cancion = tk.Label(self.frame_lista_canciones, text=cancion[1], bg="#ffffff", fg=self.label_fg, font=self.font)
                label_cancion.pack(pady=5)
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar canciones: {e}")
        finally:
            cursor.close()
            conn.close()

    def buscar_canciones(self):
        termino_busqueda = self.entry_busqueda.get()
        conn = self.conectar_db()
        cursor = conn.cursor()

        try:
            cursor.execute('SELECT * FROM Musica WHERE nombre ILIKE %s', ('%' + termino_busqueda + '%',))
            canciones = cursor.fetchall()

            for widget in self.frame_lista_canciones.winfo_children():
                widget.destroy()

            for cancion in canciones:
                label_cancion = tk.Label(self.frame_lista_canciones, text=cancion[1], bg="#ffffff", fg=self.label_fg, font=self.font)
                label_cancion.pack(pady=5)
        except Exception as e:
            messagebox.showerror("Error", f"Error al buscar canciones: {e}")
        finally:
            cursor.close()
            conn.close()

    def mostrar_playlist(self):
        messagebox.showinfo("Playlist", "Mostrando Playlist")

    def mostrar_artistas(self):
        messagebox.showinfo("Artistas", "Mostrando Artistas")

    def mostrar_albumes(self):
        messagebox.showinfo("Álbumes", "Mostrando Álbumes")

    def mostrar_genero(self):
        messagebox.showinfo("Género", "Mostrando Género")

    def clear_entry(self, event):
        if event.widget.get() in ["E-mail", "Password", "Name", "Buscar canciones..."]:
            event.widget.delete(0, tk.END)
            event.widget.config(fg=self.label_fg)

    def restore_entry(self, event, field, default):
        if not field.get():
            field.insert(0, default)
            field.config(fg="#888888")

if __name__ == "__main__":
    root = tk.Tk()
    app = Mi_Consola(root)
    root.mainloop()
