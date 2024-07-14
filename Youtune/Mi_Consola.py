import tkinter as tk
from tkinter import messagebox, Menu, simpledialog, Scale, HORIZONTAL
from PIL import Image, ImageTk
import psycopg2
import platform
import json
import os
from datetime import datetime
import pygame

class Mi_Consola:
    def __init__(self, root):
        self.root = root
        self.root.title("APLICACION - YOUTUNE")
        self.root.geometry("800x400")
        self.root.configure(bg="#f0f0f0")

        # Estilos comunes
        self.entry_bg = "#ecf0f1"
        self.label_fg = "#2c3e50"
        self.button_bg = "#2980b9"
        self.button_fg = "#ecf0f1"
        self.font = ("Helvetica", 12)

        # Variables para el reproductor de música
        pygame.mixer.init()
        self.is_playing = False
        self.track_length = 0
        self.slider_dragging = False
        self.current_playlist = []
        self.current_track_index = 0

        # Contenedor principal
        self.main_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.main_frame.pack(expand=True, fill="both")
        
        self.crear_registro()

    def clear_entry(self, event):
        if event.widget.get() in ["E-mail", "Password", "Name"]:
            event.widget.delete(0, tk.END)
            event.widget.config(fg=self.label_fg)

    def restore_entry(self, event, field, default):
        if not field.get():
            field.insert(0, default)
            field.config(fg="#888888")    

    def crear_registro(self):
        self.limpiar_frames()

        # Cargar imagen de fondo
        self.image = Image.open("C:/Users/Richard-P/Algoritmica-Avanzada/Imagenes/YOUTUNE.png")
        self.image = self.image.resize((400, 400), Image.Resampling.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(self.image)

        # Contenedor izquierdo (Registro)
        self.left_frame = tk.Frame(self.main_frame, bg="#ffffff", bd=2, relief="solid")
        self.left_frame.place(relwidth=0.5, relheight=1.0)

        self.label_sign_up = tk.Label(self.left_frame, text="REGISTRARSE", bg="#ffffff", fg=self.label_fg, font=("Helvetica", 18, "bold"))
        self.label_sign_up.pack(pady=20)

        self.entry_nombre_usuario = tk.Entry(self.left_frame, bg=self.entry_bg, font=self.font)
        self.entry_nombre_usuario.pack(pady=10, padx=20)
        self.entry_nombre_usuario.insert(0, "Name")
        self.entry_nombre_usuario.bind('<FocusIn>', self.clear_entry)
        self.entry_nombre_usuario.bind('<FocusOut>', lambda event, field=self.entry_nombre_usuario, default="Name": self.restore_entry(event, field, default))


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

        self.button_registrar_usuario = tk.Button(self.left_frame, text="Registrarse", command=self.registrar_usuario, bg="#800080", fg=self.button_fg, font=self.font)
        self.button_registrar_usuario.pack(pady=10)

        self.button_login_prompt = tk.Button(self.left_frame, text="¿Ya tienes una cuenta? Inicia sesión", command=self.crear_login, bg="#ffffff", fg=self.label_fg, font=self.font, bd=0)
        self.button_login_prompt.pack(pady=10)

        # Contenedor derecho (Bienvenida) con imagen de fondo
        self.right_frame = tk.Frame(self.main_frame, bg="#3498db", bd=2, relief="solid")
        self.right_frame.place(relx=0.5, relwidth=0.5, relheight=1.0)

        self.canvas = tk.Canvas(self.right_frame, width=400, height=400)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")

    def crear_login(self):
        self.limpiar_frames()

        # Cargar imagen de fondo
        self.image = Image.open("C:/Users/Richard-P/Algoritmica-Avanzada/Imagenes/YOUTUNE.png")
        self.image = self.image.resize((400, 400), Image.Resampling.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(self.image)

        # Contenedor derecho (Iniciar sesión)
        self.right_frame = tk.Frame(self.main_frame, bg="#ffffff", bd=2, relief="solid")
        self.right_frame.place(relwidth=0.5, relheight=1.0)

        self.label_login = tk.Label(self.right_frame, text="INICIO DE SESION", bg="#ffffff", fg=self.label_fg, font=("Helvetica", 18, "bold"))
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

        self.button_iniciar_sesion = tk.Button(self.right_frame, text="SIGN IN", command=self.iniciar_sesion, bg="#800080", fg=self.button_fg, font=self.font)
        self.button_iniciar_sesion.pack(pady=20)

        self.button_register_prompt = tk.Button(self.right_frame, text="¿No tienes una cuenta? Regístrate", command=self.crear_registro, bg="#ffffff", fg=self.label_fg, font=self.font, bd=0)
        self.button_register_prompt.pack(pady=10)

        # Contenedor izquierdo (Bienvenida) con imagen de fondo
        self.left_frame = tk.Frame(self.main_frame, bg="#3498db", bd=2, relief="solid")
        self.left_frame.place(relx=0.5, relwidth=0.5, relheight=1.0)

        self.canvas = tk.Canvas(self.left_frame, width=400, height=400)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")

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
        contrasena = self.entry_contrasena_usuario.get()
        correo = self.entry_correo_usuario.get()
        fecha_registro = datetime.now()

        conn = self.conectar_db()
        cursor = conn.cursor()

        try:
            cursor.execute('SELECT * FROM Usuario WHERE correo = %s', (correo,))
            if cursor.fetchone():
                messagebox.showerror("Error", "El correo ya está registrado")
            else:
                cursor.execute('SELECT COALESCE(MAX(id_usuario), 0) + 1 FROM Usuario')
                next_id = cursor.fetchone()[0]

                cursor.execute('''
                INSERT INTO Usuario (id_usuario, nombre, contrasena, correo, fecha_registro) 
                VALUES (%s, %s, %s, %s, %s)
                ''', (next_id, nombre, contrasena, correo, fecha_registro))
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
            cursor.execute('SELECT * FROM Usuario WHERE correo = %s AND contrasena = %s', (correo, contrasena))
            usuario = cursor.fetchone()

            if usuario:
                messagebox.showinfo("Éxito", f"Bienvenido {usuario[1]}")

                # Guardar el nombre, correo y id del usuario en variables de instancia
                self.nombre_usuario = usuario[1]
                self.correo_usuario = usuario[3]
                self.id_usuario = usuario[0]

                # Capturar el dispositivo desde el cual se inicia sesión
                dispositivo = platform.node()

                # Verificar si el dispositivo ya está registrado para el usuario actual
                cursor.execute('''
                    SELECT d.id_dispositivo FROM Dispositivos d
                    JOIN Usuario_Dispositivos ud ON d.id_dispositivo = ud.id_dispositivo
                    WHERE ud.id_usuario = %s AND d.nombre = %s
                ''', (self.id_usuario, dispositivo))
                dispositivo_registrado = cursor.fetchone()

                if dispositivo_registrado:
                    # El dispositivo ya está registrado, usar el id existente
                    self.id_dispositivo_actual = dispositivo_registrado[0]
                else:
                    # Obtener el siguiente ID para dispositivos
                    cursor.execute('SELECT MAX(id_dispositivo) FROM Dispositivos')
                    max_id_result = cursor.fetchone()[0]
                    next_id = max_id_result + 1 if max_id_result is not None else 1

                    # Registrar el dispositivo en la tabla Dispositivos
                    cursor.execute('INSERT INTO Dispositivos (id_dispositivo, nombre) VALUES (%s, %s)', (next_id, dispositivo))
                    conn.commit()

                    # Registrar la relación en la tabla Usuario_Dispositivos
                    cursor.execute('INSERT INTO Usuario_Dispositivos (id_usuario, id_dispositivo) VALUES (%s, %s)', (self.id_usuario, next_id))
                    conn.commit()

                    self.id_dispositivo_actual = next_id

                self.mostrar_panel_canciones()
                self.redimensionar_imagen_fondo()
            else:
                messagebox.showerror("Error", "Correo o contraseña incorrectos")
        except Exception as e:
            messagebox.showerror("Error", f"Error al iniciar sesión: {e}")
        finally:
            cursor.close()
            conn.close() 


    def mostrar_historial(self):
        self.limpiar_frames()

        self.frame_historial = tk.Frame(self.main_frame, bg="#ffffff")
        self.frame_historial.pack(expand=True, fill="both")

        self.label_historial = tk.Label(self.frame_historial, text="Historial de Reproducción", bg="#ffffff", fg=self.label_fg, font=("Helvetica", 18, "bold"))
        self.label_historial.pack(pady=20)

        # Crear un contenedor para el canvas y el scrollbar
        canvas_frame = tk.Frame(self.frame_historial, bg="#ffffff")
        canvas_frame.pack(expand=True, fill="both")

        # Crear un canvas y agregar el scrollbar
        self.canvas_historial = tk.Canvas(canvas_frame, bg="#ffffff")
        scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=self.canvas_historial.yview)
        self.canvas_historial.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        self.canvas_historial.pack(side="left", expand=True, fill="both")

        # Crear un Frame dentro del canvas
        self.scrollable_frame_historial = tk.Frame(self.canvas_historial, bg="#ffffff")
        self.canvas_historial.create_window((0, 0), window=self.scrollable_frame_historial, anchor="nw")

        self.scrollable_frame_historial.bind("<Configure>", lambda e: self.canvas_historial.configure(scrollregion=self.canvas_historial.bbox("all")))

        conn = self.conectar_db()
        cursor = conn.cursor()

        try:
            cursor.execute('SELECT * FROM obtener_historial_usuario(%s)', (self.id_usuario,))
            historial = cursor.fetchall()

            for entrada in historial:
                nombre_cancion = entrada[0]
                label_historial = tk.Label(self.scrollable_frame_historial, text=f"{nombre_cancion} - {entrada[1]} - {entrada[2]}", bg="#ffffff", fg=self.label_fg, font=self.font)
                label_historial.pack(pady=5, fill="x")

                # Eventos para cambiar el color del fondo al pasar el cursor
                label_historial.bind("<Enter>", lambda event, lbl=label_historial: lbl.config(bg="#d1e0ff"))
                label_historial.bind("<Leave>", lambda event, lbl=label_historial: lbl.config(bg="#ffffff"))

                # Evento para reproducir la canción al hacer clic
                label_historial.bind("<Button-1>", lambda event, song_name=nombre_cancion: self.reproducir_cancion_desde_carpeta(song_name))

        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar historial: {e}")
        finally:
            cursor.close()
            conn.close() 

    def redimensionar_imagen_fondo(self):
        if self.image_label:
            # Redimensionar la imagen
            self.image = Image.open("C:/Users/Richard-P/Algoritmica-Avanzada/Imagenes/YoutuneII.png")
            self.image = self.image.resize((self.frame_canciones.winfo_width(), self.frame_canciones.winfo_height()), Image.Resampling.LANCZOS)
            self.bg_image = ImageTk.PhotoImage(self.image)
            self.image_label.config(image=self.bg_image)
            
    def mostrar_panel_canciones(self):
        self.limpiar_frames()

        self.frame_canciones = tk.Frame(self.main_frame, bg="#ffffff")
        self.frame_canciones.pack(expand=True, fill="both")
        
        # Cargar imagen de fondo
        self.image = Image.open("C:/Users/Richard-P/Algoritmica-Avanzada/Imagenes/YoutuneII.png")
        self.image = self.image.resize((self.frame_canciones.winfo_width(), self.frame_canciones.winfo_height()), Image.Resampling.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(self.image)
        
        # Colocar la imagen de fondo en un label
        self.image_label = tk.Label(self.frame_canciones, image=self.bg_image)
        self.image_label.place(relwidth=1, relheight=1)
        
        # Menú
        self.menu_bar = Menu(self.root)
        self.root.config(menu=self.menu_bar)

        self.menu_perfil = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Perfil", menu=self.menu_perfil)
        self.menu_perfil.add_command(label="Mostrar Perfil", command=self.mostrar_perfil)
        self.menu_perfil.add_command(label="Cambiar Nombre", command=self.cambiar_nombre)
        self.menu_perfil.add_command(label="Cambiar Contraseña", command=self.cambiar_contrasena)
        self.menu_perfil.add_separator()
        self.menu_perfil.add_command(label="Cerrar Sesión", command=self.cerrar_sesion)

        # Resto de las opciones del menú...
        self.menu_playlist = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Playlist", menu=self.menu_playlist)
        self.menu_playlist.add_command(label="Mostrar Playlists", command=self.mostrar_playlists)
        self.menu_playlist.add_command(label="Crear Playlist", command=self.crear_nueva_playlist)

        self.menu_musica = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Música", menu=self.menu_musica)
        self.menu_musica.add_command(label="Buscar Canciones", command=self.buscar_canciones)

        self.menu_artistas = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_command(label="Artistas", command=self.mostrar_artistas)

        self.menu_albumes = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_command(label="Álbumes", command=self.mostrar_albumes)

        self.menu_genero = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_command(label="Género", command=self.mostrar_genero)

        self.menu_historial = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_command(label="Historial", command=self.mostrar_historial)
        
        self.frame_canciones.bind("<Configure>", lambda e: self.redimensionar_imagen_fondo())
        
        self.crear_reproductor()
        


    def crear_reproductor(self):
     self.frame_reproductor = tk.Frame(self.root, bg="#800080")
     self.frame_reproductor.pack(side="bottom", fill="x")

     self.button_previous = tk.Button(self.frame_reproductor, text="<<", command=self.anterior_musica,  bg="#ffffff", fg="#000000", font=self.font)
     self.button_previous.pack(side="left", padx=5, pady=5)

     self.button_play_pause = tk.Button(self.frame_reproductor, text="Play", command=self.play_pause_musica, bg="#ffffff", fg="#000000", font=self.font)
     self.button_play_pause.pack(side="left", padx=5, pady=5)

     self.button_next = tk.Button(self.frame_reproductor, text=">>", command=self.siguiente_musica, bg="#ffffff", fg="#000000", font=self.font)
     self.button_next.pack(side="left", padx=5, pady=5)

     self.scale = Scale(self.frame_reproductor, from_=0, to=100, orient=HORIZONTAL, length=400, bg="#800080", fg=self.button_fg, font=self.font, showvalue=0)
     self.scale.pack(side="left", fill="x", expand=True, padx=5)
     self.scale.bind("<ButtonPress-1>", self.empezar_arrastrar_slider)
     self.scale.bind("<ButtonRelease-1>", self.soltar_slider)
     self.scale.bind("<B1-Motion>", self.actualizar_tiempo_slider)

     self.label_tiempo = tk.Label(self.frame_reproductor, text="00:00 / 00:00", bg="#800080", fg=self.button_fg, font=self.font)
     self.label_tiempo.pack(side="left", padx=5, pady=5)

    # Añadir escala de volumen
     self.volumen = Scale(self.frame_reproductor, from_=0, to=1, resolution=0.01, orient=HORIZONTAL, length=100, bg="#800080", fg=self.button_fg, font=self.font)
     self.volumen.set(0.5)  # Valor inicial del volumen (50%)
     self.volumen.pack(side="right", padx=5, pady=5)
     self.volumen.bind("<Motion>", self.ajustar_volumen)

    def ajustar_volumen(self, event=None):
     volumen = self.volumen.get()
     pygame.mixer.music.set_volume(volumen)

    
    def cambiar_nombre(self):
     nuevo_nombre = simpledialog.askstring("Cambiar Nombre", "Ingrese su nuevo nombre:")
     if nuevo_nombre:
         conn = self.conectar_db()
         cursor = conn.cursor()
         try:
             cursor.execute('UPDATE Usuario SET nombre = %s WHERE id_usuario = %s', (nuevo_nombre, self.id_usuario))
             conn.commit()
             self.nombre_usuario = nuevo_nombre
             messagebox.showinfo("Éxito", "Nombre cambiado con éxito.")
         except Exception as e:
             messagebox.showerror("Error", f"No se pudo cambiar el nombre: {e}")
         finally:
             cursor.close()
             conn.close()

    def cambiar_contrasena(self):
     nueva_contrasena = simpledialog.askstring("Cambiar Contraseña", "Ingrese su nueva contraseña:", show="*")
     if nueva_contrasena:
         conn = self.conectar_db()
         cursor = conn.cursor()
         try:
             cursor.execute('UPDATE Usuario SET contrasena = %s WHERE id_usuario = %s', (nueva_contrasena, self.id_usuario))
             conn.commit()
             messagebox.showinfo("Éxito", "Contraseña cambiada con éxito.")
         except Exception as e:
             messagebox.showerror("Error", f"No se pudo cambiar la contraseña: {e}")
         finally:
             cursor.close()
             conn.close()
     
    def crear_nueva_playlist(self):
        nombre_playlist = simpledialog.askstring("Crear Playlist", "Ingrese el nombre de la nueva playlist")
        if nombre_playlist:
            privacidad = messagebox.askyesno("Privacidad", "¿Desea que la playlist sea privada?")
            privacidad = True if privacidad else False

            conn = self.conectar_db()
            cursor = conn.cursor()

            try:
                cursor.execute("CALL crear_playlist(%s, %s, %s)", (self.id_usuario, nombre_playlist, privacidad))
                conn.commit()
                messagebox.showinfo("Éxito", f"Playlist '{nombre_playlist}' creada correctamente.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo crear la playlist: {e}")
            finally:
                cursor.close()
                conn.close()

    def mostrar_perfil(self):
        self.limpiar_frames()
        
        self.label_nombre = tk.Label(self.main_frame, text=f"Nombre: {self.nombre_usuario}", font=self.font, bg="#f0f0f0")
        self.label_nombre.pack(pady=10)

        self.label_correo = tk.Label(self.main_frame, text=f"Correo: {self.correo_usuario}", font=self.font, bg="#f0f0f0")
        self.label_correo.pack(pady=10)
        
    def cerrar_sesion(self):
     self.nombre_usuario = None
     self.correo_usuario = None

    # Detener la música si está reproduciéndose
     if self.is_playing:
         pygame.mixer.music.stop()
         self.is_playing = False

    # Destruir el reproductor
     self.frame_reproductor.destroy()

    # Limpiar y volver a la pantalla de registro/inicio de sesión
     self.menu_bar.delete(0, tk.END)
     self.crear_registro()


    def mostrar_playlists(self):
        self.limpiar_frames()

        self.frame_playlists = tk.Frame(self.main_frame, bg="#ffffff")
        self.frame_playlists.pack(expand=True, fill="both")

        self.label_playlists = tk.Label(self.frame_playlists, text="Todas las Playlists", bg="#ffffff", fg=self.label_fg, font=("Helvetica", 18, "bold"))
        self.label_playlists.pack(pady=20)

        canvas_frame = tk.Frame(self.frame_playlists, bg="#ffffff")
        canvas_frame.pack(expand=True, fill="both")

        self.canvas_playlists = tk.Canvas(canvas_frame, bg="#ffffff")
        scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=self.canvas_playlists.yview)
        self.canvas_playlists.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        self.canvas_playlists.pack(side="left", expand=True, fill="both")

        self.scrollable_frame_playlists = tk.Frame(self.canvas_playlists, bg="#ffffff")
        self.canvas_playlists.create_window((0, 0), window=self.scrollable_frame_playlists, anchor="nw")

        self.scrollable_frame_playlists.bind("<Configure>", lambda e: self.canvas_playlists.configure(scrollregion=self.canvas_playlists.bbox("all")))

        conn = self.conectar_db()
        cursor = conn.cursor()

        try:
            cursor.execute('SELECT * FROM obtener_playlists_publicas_privadas(%s)', (self.id_usuario,))
            playlists = cursor.fetchall()

            for playlist in playlists:
                label_playlist = tk.Label(self.scrollable_frame_playlists, text=playlist[1], bg="#ffffff", fg=self.label_fg, font=self.font, pady=10)
                label_playlist.pack(pady=5, fill="x")

                label_playlist.bind("<Enter>", lambda event, lbl=label_playlist: lbl.config(bg="#d1e0ff"))
                label_playlist.bind("<Leave>", lambda event, lbl=label_playlist: lbl.config(bg="#ffffff"))

                label_playlist.bind("<Button-1>", lambda event, playlist_id=playlist[0]: self.mostrar_canciones_playlist(playlist_id))
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar playlists: {e}")
        finally:
            cursor.close()
            conn.close()

    def mostrar_artistas(self):
     self.limpiar_frames()

     self.frame_artistas = tk.Frame(self.main_frame, bg="#ffffff")
     self.frame_artistas.pack(expand=True, fill="both")

     self.label_titulo_artistas = tk.Label(self.frame_artistas, text="Artistas", bg="#ffffff", fg=self.label_fg, font=("Helvetica", 18, "bold"))
     self.label_titulo_artistas.pack(pady=20)

     frame = tk.Frame(self.main_frame, bg="#ffffff")
     frame.pack(fill="both", expand=True)

     canvas = tk.Canvas(frame, bg="#ffffff")
     scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
     scrollable_frame = tk.Frame(canvas, bg="#ffffff")

     scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

     canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
     canvas.configure(yscrollcommand=scrollbar.set)

     canvas.pack(side="left", fill="both", expand=True)
     scrollbar.pack(side="right", fill="y")

     conn = self.conectar_db()
     cursor = conn.cursor()
     cursor.execute('SELECT * FROM Artista')
     artistas = cursor.fetchall()

     for artista in artistas:
         label_artista = tk.Label(scrollable_frame, text=f"{artista[1]}", bg="#ffffff", fg=self.label_fg, font=self.font)
         label_artista.pack(pady=10, fill="x")

        # Eventos para cambiar el color del fondo al pasar el cursor
         label_artista.bind("<Enter>", lambda event, lbl=label_artista: lbl.config(bg="#d1e0ff"))
         label_artista.bind("<Leave>", lambda event, lbl=label_artista: lbl.config(bg="#ffffff"))

         label_artista.bind("<Button-1>", lambda event, artista_id=artista[0]: self.mostrar_canciones_por_artista(artista_id))

     cursor.close()
     conn.close()


    def mostrar_albumes(self):
     self.limpiar_frames()

     self.frame_albumes = tk.Frame(self.main_frame, bg="#ffffff")
     self.frame_albumes.pack(expand=True, fill="both")

     self.label_titulo_albumes = tk.Label(self.frame_albumes, text="Álbumes", bg="#ffffff", fg=self.label_fg, font=("Helvetica", 18, "bold"))
     self.label_titulo_albumes.pack(pady=20)

     canvas_frame = tk.Frame(self.frame_albumes, bg="#ffffff")
     canvas_frame.pack(expand=True, fill="both")

     self.canvas_albumes = tk.Canvas(canvas_frame, bg="#ffffff")
     scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=self.canvas_albumes.yview)
     self.canvas_albumes.configure(yscrollcommand=scrollbar.set)

     scrollbar.pack(side="right", fill="y")
     self.canvas_albumes.pack(side="left", expand=True, fill="both")

     self.scrollable_frame_albumes = tk.Frame(self.canvas_albumes, bg="#ffffff")
     self.canvas_albumes.create_window((0, 0), window=self.scrollable_frame_albumes, anchor="nw")

     self.scrollable_frame_albumes.bind("<Configure>", lambda e: self.canvas_albumes.configure(scrollregion=self.canvas_albumes.bbox("all")))

     conn = self.conectar_db()
     cursor = conn.cursor()

     try:
         cursor.execute('SELECT * FROM Album')
         albumes = cursor.fetchall()

         for album in albumes:
             label_album = tk.Label(self.scrollable_frame_albumes, text=album[1], bg="#ffffff", fg=self.label_fg, font=self.font)
             label_album.pack(pady=5, fill="x")

            # Eventos para cambiar el color del fondo al pasar el cursor
             label_album.bind("<Enter>", lambda event, lbl=label_album: lbl.config(bg="#d1e0ff"))
             label_album.bind("<Leave>", lambda event, lbl=label_album: lbl.config(bg="#ffffff"))

             label_album.bind("<Button-1>", lambda event, album_id=album[0]: self.mostrar_canciones_por_album(album_id))


     except Exception as e:
         messagebox.showerror("Error", f"Error al cargar álbumes: {e}")
     finally:
         cursor.close()
         conn.close()
 
    def mostrar_genero(self):
     self.limpiar_frames()

     self.frame_genero = tk.Frame(self.main_frame, bg="#ffffff")
     self.frame_genero.pack(expand=True, fill="both")

     self.label_titulo_genero = tk.Label(self.frame_genero, text="Género", bg="#ffffff", fg=self.label_fg, font=("Helvetica", 18, "bold"))
     self.label_titulo_genero.pack(pady=20)

     canvas_frame = tk.Frame(self.frame_genero, bg="#ffffff")
     canvas_frame.pack(expand=True, fill="both")

     self.canvas_genero = tk.Canvas(canvas_frame, bg="#ffffff")
     scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=self.canvas_genero.yview)
     self.canvas_genero.configure(yscrollcommand=scrollbar.set)

     scrollbar.pack(side="right", fill="y")
     self.canvas_genero.pack(side="left", expand=True, fill="both")

     self.scrollable_frame_genero = tk.Frame(self.canvas_genero, bg="#ffffff")
     self.canvas_genero.create_window((0, 0), window=self.scrollable_frame_genero, anchor="nw")

     self.scrollable_frame_genero.bind("<Configure>", lambda e: self.canvas_genero.configure(scrollregion=self.canvas_genero.bbox("all")))

     conn = self.conectar_db()
     cursor = conn.cursor()

     try:
         cursor.execute('SELECT * FROM Genero')
         generos = cursor.fetchall()

         for genero in generos:
             label_genero = tk.Label(self.scrollable_frame_genero, text=genero[1], bg="#ffffff", fg=self.label_fg, font=self.font)
             label_genero.pack(pady=5, fill="x")
 
             # Eventos para cambiar el color del fondo al pasar el cursor
             label_genero.bind("<Enter>", lambda event, lbl=label_genero: lbl.config(bg="#d1e0ff"))
             label_genero.bind("<Leave>", lambda event, lbl=label_genero: lbl.config(bg="#ffffff"))
           
             label_genero.bind("<Button-1>", lambda event, genero_id=genero[0]: self.mostrar_canciones_por_genero(genero_id))

     except Exception as e:
         messagebox.showerror("Error", f"Error al cargar géneros: {e}")
     finally:
         cursor.close()
         conn.close()


    def buscar_canciones(self):
        self.limpiar_frames()

        self.frame_canciones = tk.Frame(self.main_frame, bg="#ffffff")
        self.frame_canciones.pack(expand=True, fill="both")

        self.frame_busqueda = tk.Frame(self.frame_canciones, bg="#ffffff")
        self.frame_busqueda.pack(padx=20, pady=10, fill="x")

        self.entry_busqueda = tk.Entry(self.frame_busqueda, width=40, font=self.font, bg=self.entry_bg, fg=self.label_fg)
        self.entry_busqueda.pack(side="left", padx=5)

        self.button_buscar = tk.Button(self.frame_busqueda, text="Buscar", font=self.font, bg=self.button_bg, fg=self.button_fg, command=self.realizar_busqueda)
        self.button_buscar.pack(side="left", padx=5)

        canvas_frame = tk.Frame(self.frame_canciones, bg="#ffffff")
        canvas_frame.pack(expand=True, fill="both")

        self.canvas_canciones = tk.Canvas(canvas_frame, bg="#ffffff")
        scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=self.canvas_canciones.yview)
        self.canvas_canciones.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        self.canvas_canciones.pack(side="left", expand=True, fill="both")

        self.scrollable_frame_canciones = tk.Frame(self.canvas_canciones, bg="#ffffff")
        self.canvas_canciones.create_window((0, 0), window=self.scrollable_frame_canciones, anchor="nw")

        self.scrollable_frame_canciones.bind("<Configure>", lambda e: self.canvas_canciones.configure(scrollregion=self.canvas_canciones.bbox("all")))

    def realizar_busqueda(self):
        termino_busqueda = self.entry_busqueda.get()

        conn = self.conectar_db()
        cursor = conn.cursor()

        try:
            cursor.execute('SELECT * FROM Musica WHERE nombre LIKE %s', ('%' + termino_busqueda + '%',))
            canciones_encontradas = cursor.fetchall()

            for widget in self.scrollable_frame_canciones.winfo_children():
                widget.destroy()

            if not canciones_encontradas:
                messagebox.showinfo("Info", "No se encontraron canciones.")
            else:
                self.current_playlist = [cancion[1] for cancion in canciones_encontradas]
                self.current_track_index = 0
                for cancion in canciones_encontradas:
                    label_cancion = tk.Label(self.scrollable_frame_canciones, text=cancion[1], bg="#ffffff", fg=self.label_fg, font=self.font, pady=10)
                    label_cancion.pack(pady=5, fill="x")

                    label_cancion.bind("<Enter>", lambda event, lbl=label_cancion: lbl.config(bg="#d1e0ff"))
                    label_cancion.bind("<Leave>", lambda event, lbl=label_cancion: lbl.config(bg="#ffffff"))

                    label_cancion.bind("<Button-1>", lambda event, song_name=cancion[1]: self.reproducir_cancion_desde_carpeta(song_name))

        except Exception as e:
            messagebox.showerror("Error", f"Error al realizar búsqueda: {e}")
        finally:
            cursor.close()
            conn.close()

    def reproducir_cancion_desde_carpeta(self, song_name):
        carpeta_musica = "C:/Users/Richard-P/Algoritmica-Avanzada/Musicas"
        archivo_musica = os.path.join(carpeta_musica, f"{song_name}.mp3")

        if os.path.isfile(archivo_musica):
            # Cargar la música en pygame.mixer.music

            pygame.mixer.music.load(archivo_musica)
            pygame.mixer.music.play()
            self.is_playing = True

            # Obtener el ID del dispositivo actual
            id_dispositivo_actual = self.id_dispositivo_actual

            # Obtener el ID de la música actual desde la base de datos
            conn = self.conectar_db()
            cursor = conn.cursor()

            try:
                cursor.execute('SELECT id_musica FROM Musica WHERE nombre = %s', (song_name,))
                id_musica_actual = cursor.fetchone()[0]
            except Exception as e:
                messagebox.showerror("Error", f"Error al obtener ID de la música: {e}")
                return
            finally:
                cursor.close()
                conn.close()

            # Verificar si la música está en el historial
            conn = self.conectar_db()
            cursor = conn.cursor()

            try:
                cursor.execute('SELECT COUNT(*) FROM Historial WHERE id_dispositivo = %s AND id_musica = %s', (id_dispositivo_actual, id_musica_actual))
                existe_en_historial = cursor.fetchone()[0] > 0
            except Exception as e:
                messagebox.showerror("Error", f"Error al verificar historial: {e}")
                return
            finally:
                cursor.close()
                conn.close()

            # Ejecutar el comando correspondiente según el resultado
            if not existe_en_historial:
                # Ejecutar el procedimiento almacenado para insertar en el historial
                conn = self.conectar_db()
                cursor = conn.cursor()
                try:
                    cursor.execute("CALL insertar_historial(%s, %s, current_timestamp)", (id_dispositivo_actual, id_musica_actual))
                    conn.commit()
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo insertar en historial: {e}")
                finally:
                    cursor.close()
                    conn.close()
            else:
                # Ejecutar la función para actualizar fecha en el historial
                conn = self.conectar_db()
                cursor = conn.cursor()
                try:
                    cursor.execute("SELECT actualizar_fecha_historial(%s, %s, current_timestamp)", (id_dispositivo_actual, id_musica_actual))
                    conn.commit()
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo actualizar fecha en historial: {e}")
                finally:
                    cursor.close()
                    conn.close()

            # Resto de tu lógica de reproducción y UI
            self.track_length = pygame.mixer.Sound(archivo_musica).get_length()
            self.scale.config(to=self.track_length)
            self.actualizar_tiempo()
            messagebox.showinfo("Reproducción", f"Reproduciendo: {song_name}")
        else:
            messagebox.showerror("Error", f"No se encontró el archivo: {song_name}.mp3") 
        
    def obtener_id_dispositivo_actual(self,id_usuario):
        conn = self.conectar_db()  # Conecta a la base de datos según tu implementación
        cursor = conn.cursor()
        try:
            # Ejemplo: Obtener el primer dispositivo asociado al usuario
            cursor.execute("SELECT id_dispositivo FROM Usuario_Dispositivos WHERE id_usuario = %s LIMIT 1", (id_usuario,))
            id_dispositivo_actual = cursor.fetchone()[0]  # Suponiendo que devuelve el ID del dispositivo

            return id_dispositivo_actual
        except Exception as e:
                messagebox.showerror("Error", f"Error al obtener ID del dispositivo: {e}")
                return None
        finally:
                cursor.close()
                conn.close()


    def registrar_reproduccion(self, song_name):
        # Obtener el ID del dispositivo actual (simulado aquí como 1)
        id_dispositivo_actual = 1

        # Obtener el ID de la música actual desde la base de datos
        self.cursor.execute("SELECT id_musica FROM Musica WHERE nombre = %s", (song_name,))
        result = self.cursor.fetchone()
        if result:
            id_musica_actual = result[0]
        else:
            messagebox.showerror("Error", f"No se encontró la música en la base de datos: {song_name}")
            return

        # Verificar si la canción ya está en el historial
        self.cursor.execute("SELECT COUNT(*) FROM Historial WHERE id_musica = %s AND id_dispositivo = %s", (id_musica_actual, id_dispositivo_actual))
        count = self.cursor.fetchone()[0]

        if count == 0:
            # Insertar en el historial si no existe
            self.cursor.execute("INSERT INTO Historial (id_dispositivo, id_musica, fecha_historial) VALUES (%s, %s, %s)",
                                (id_dispositivo_actual, id_musica_actual, datetime.now()))
        else:
            # Actualizar la fecha en el historial si ya existe
            self.cursor.execute("UPDATE Historial SET fecha_historial = %s WHERE id_dispositivo = %s AND id_musica = %s",
                                (datetime.now(), id_dispositivo_actual, id_musica_actual))

        self.conn.commit()


    def mostrar_canciones_playlist(self, playlist_id):
     self.limpiar_frames()

     self.frame_canciones_playlist = tk.Frame(self.main_frame, bg="#ffffff")
     self.frame_canciones_playlist.pack(expand=True, fill="both")

     self.label_canciones_playlist = tk.Label(self.frame_canciones_playlist, text=f"Canciones de Playlist ID: {playlist_id}", bg="#ffffff", fg=self.label_fg, font=("Helvetica", 18, "bold"))
     self.label_canciones_playlist.pack(pady=20)

    # Crear un contenedor para el canvas y el scrollbar
     canvas_frame = tk.Frame(self.frame_canciones_playlist, bg="#ffffff")
     canvas_frame.pack(expand=True, fill="both")

    # Crear un canvas y agregar el scrollbar
     self.canvas_canciones_playlist = tk.Canvas(canvas_frame, bg="#ffffff")
     scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=self.canvas_canciones_playlist.yview)
     self.canvas_canciones_playlist.configure(yscrollcommand=scrollbar.set)

     scrollbar.pack(side="right", fill="y")
     self.canvas_canciones_playlist.pack(side="left", expand=True, fill="both")

    # Crear un Frame dentro del canvas
     self.scrollable_frame_canciones_playlist = tk.Frame(self.canvas_canciones_playlist, bg="#ffffff")
     self.canvas_canciones_playlist.create_window((0, 0), window=self.scrollable_frame_canciones_playlist, anchor="nw")

     self.scrollable_frame_canciones_playlist.bind("<Configure>", lambda e: self.canvas_canciones_playlist.configure(scrollregion=self.canvas_canciones_playlist.bbox("all")))

     conn = self.conectar_db()
     cursor = conn.cursor()

     try:
         cursor.execute('SELECT * FROM obtener_canciones_por_playlist(%s)', (playlist_id,))
         canciones = cursor.fetchall()

         self.current_playlist = [cancion[1] for cancion in canciones]
         self.current_track_index = 0

         for cancion in canciones:
             label_cancion = tk.Label(self.scrollable_frame_canciones_playlist, text=cancion[1], bg="#ffffff", fg=self.label_fg, font=self.font)
             label_cancion.pack(pady=5, fill="x")

            # Eventos para cambiar el color del fondo al pasar el cursor
             label_cancion.bind("<Enter>", lambda event, lbl=label_cancion: lbl.config(bg="#d1e0ff"))
             label_cancion.bind("<Leave>", lambda event, lbl=label_cancion: lbl.config(bg="#ffffff"))

            # Evento para reproducir la canción al hacer clic
             label_cancion.bind("<Button-1>", lambda event, song_name=cancion[1]: self.reproducir_cancion_desde_carpeta(song_name))

     except Exception as e:
         messagebox.showerror("Error", f"Error al cargar canciones de la playlist: {e}")
     finally:
         cursor.close()
         conn.close()


    def mostrar_canciones_por_artista(self, artista_id):
     self.limpiar_frames()

     self.frame_canciones_artista = tk.Frame(self.main_frame, bg="#ffffff")
     self.frame_canciones_artista.pack(expand=True, fill="both")

     self.label_canciones_artista = tk.Label(self.frame_canciones_artista, text=f"Canciones del Artista ID: {artista_id}", bg="#ffffff", fg=self.label_fg, font=("Helvetica", 18, "bold"))
     self.label_canciones_artista.pack(pady=20)

    # Crear un contenedor para el canvas y el scrollbar
     canvas_frame = tk.Frame(self.frame_canciones_artista, bg="#ffffff")
     canvas_frame.pack(expand=True, fill="both")

    # Crear un canvas y agregar el scrollbar
     self.canvas_canciones_artista = tk.Canvas(canvas_frame, bg="#ffffff")
     scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=self.canvas_canciones_artista.yview)
     self.canvas_canciones_artista.configure(yscrollcommand=scrollbar.set)

     scrollbar.pack(side="right", fill="y")
     self.canvas_canciones_artista.pack(side="left", expand=True, fill="both")

    # Crear un Frame dentro del canvas
     self.scrollable_frame_canciones_artista = tk.Frame(self.canvas_canciones_artista, bg="#ffffff")
     self.canvas_canciones_artista.create_window((0, 0), window=self.scrollable_frame_canciones_artista, anchor="nw")

     self.scrollable_frame_canciones_artista.bind("<Configure>", lambda e: self.canvas_canciones_artista.configure(scrollregion=self.canvas_canciones_artista.bbox("all")))

     conn = self.conectar_db()
     cursor = conn.cursor()

     try:
         cursor.execute('SELECT nombre_cancion, fecha_lanzamiento, visualizaciones FROM canciones_por_artista(%s)', (artista_id,))
         canciones = cursor.fetchall()

         self.current_playlist = [cancion[0] for cancion in canciones]
         self.current_track_index = 0

         for cancion in canciones:
             nombre, fecha, visualizaciones = cancion
             label_cancion = tk.Label(self.scrollable_frame_canciones_artista, text=f"{nombre} - {fecha} - {visualizaciones} visualizaciones", bg="#ffffff", fg=self.label_fg, font=self.font)
             label_cancion.pack(pady=5, fill="x")

            # Eventos para cambiar el color del fondo al pasar el cursor
             label_cancion.bind("<Enter>", lambda event, lbl=label_cancion: lbl.config(bg="#d1e0ff"))
             label_cancion.bind("<Leave>", lambda event, lbl=label_cancion: lbl.config(bg="#ffffff"))

             label_cancion.bind("<Button-1>", lambda event, song_name=nombre: self.reproducir_cancion_desde_carpeta(song_name))

     except Exception as e:
         messagebox.showerror("Error", f"Error al cargar canciones del artista: {e}")
     finally:
         cursor.close()
         conn.close()
  
    def mostrar_canciones_por_album(self, album_id):
     self.limpiar_frames()

     self.frame_canciones_album = tk.Frame(self.main_frame, bg="#ffffff")
     self.frame_canciones_album.pack(expand=True, fill="both")

     self.label_canciones_album = tk.Label(self.frame_canciones_album, text=f"Canciones del Álbum ID: {album_id}", bg="#ffffff", fg=self.label_fg, font=("Helvetica", 18, "bold"))
     self.label_canciones_album.pack(pady=20)

    # Crear un contenedor para el canvas y el scrollbar
     canvas_frame = tk.Frame(self.frame_canciones_album, bg="#ffffff")
     canvas_frame.pack(expand=True, fill="both")

    # Crear un canvas y agregar el scrollbar
     self.canvas_canciones_album = tk.Canvas(canvas_frame, bg="#ffffff")
     scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=self.canvas_canciones_album.yview)
     self.canvas_canciones_album.configure(yscrollcommand=scrollbar.set)

     scrollbar.pack(side="right", fill="y")
     self.canvas_canciones_album.pack(side="left", expand=True, fill="both")

    # Crear un Frame dentro del canvas
     self.scrollable_frame_canciones_album = tk.Frame(self.canvas_canciones_album, bg="#ffffff")
     self.canvas_canciones_album.create_window((0, 0), window=self.scrollable_frame_canciones_album, anchor="nw")

     self.scrollable_frame_canciones_album.bind("<Configure>", lambda e: self.canvas_canciones_album.configure(scrollregion=self.canvas_canciones_album.bbox("all")))

     conn = self.conectar_db()
     cursor = conn.cursor()

     try:
         cursor.execute('SELECT nombre_musica FROM canciones_por_album(%s)', (album_id,))
         canciones = cursor.fetchall()

         self.current_playlist = [cancion[0] for cancion in canciones]
         self.current_track_index = 0

         for cancion in canciones:
             nombre = cancion[0]
             label_cancion = tk.Label(self.scrollable_frame_canciones_album, text=f"{nombre}", bg="#ffffff", fg=self.label_fg, font=self.font)
             label_cancion.pack(pady=5, fill="x")
 
            # Eventos para cambiar el color del fondo al pasar el cursor
             label_cancion.bind("<Enter>", lambda event, lbl=label_cancion: lbl.config(bg="#d1e0ff"))
             label_cancion.bind("<Leave>", lambda event, lbl=label_cancion: lbl.config(bg="#ffffff"))
 
             label_cancion.bind("<Button-1>", lambda event, song_name=nombre: self.reproducir_cancion_desde_carpeta(song_name))

     except Exception as e:
         messagebox.showerror("Error", f"Error al cargar canciones del álbum: {e}")
     finally:
         cursor.close()
         conn.close()
         
    def mostrar_canciones_por_genero(self, genero_id):
     self.limpiar_frames()

     self.frame_canciones_genero = tk.Frame(self.main_frame, bg="#ffffff")
     self.frame_canciones_genero.pack(expand=True, fill="both")

     self.label_canciones_genero = tk.Label(self.frame_canciones_genero, text=f"Canciones del Género ID: {genero_id}", bg="#ffffff", fg=self.label_fg, font=("Helvetica", 18, "bold"))
     self.label_canciones_genero.pack(pady=20)

    # Crear un contenedor para el canvas y el scrollbar
     canvas_frame = tk.Frame(self.frame_canciones_genero, bg="#ffffff")
     canvas_frame.pack(expand=True, fill="both")

    # Crear un canvas y agregar el scrollbar
     self.canvas_canciones_genero = tk.Canvas(canvas_frame, bg="#ffffff")
     scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=self.canvas_canciones_genero.yview)
     self.canvas_canciones_genero.configure(yscrollcommand=scrollbar.set)

     scrollbar.pack(side="right", fill="y")
     self.canvas_canciones_genero.pack(side="left", expand=True, fill="both")

    # Crear un Frame dentro del canvas
     self.scrollable_frame_canciones_genero = tk.Frame(self.canvas_canciones_genero, bg="#ffffff")
     self.canvas_canciones_genero.create_window((0, 0), window=self.scrollable_frame_canciones_genero, anchor="nw")

     self.scrollable_frame_canciones_genero.bind("<Configure>", lambda e: self.canvas_canciones_genero.configure(scrollregion=self.canvas_canciones_genero.bbox("all")))

     conn = self.conectar_db()
     cursor = conn.cursor()

     try:
         cursor.execute('SELECT nombre_musica FROM canciones_por_genero(%s)', (genero_id,))
         canciones = cursor.fetchall()

         self.current_playlist = [cancion[0] for cancion in canciones]
         self.current_track_index = 0

         for cancion in canciones:
             nombre = cancion[0]  # Desempaqueta la tupla correctamente
             label_cancion = tk.Label(self.scrollable_frame_canciones_genero, text=nombre, bg="#ffffff", fg=self.label_fg, font=self.font)
             label_cancion.pack(pady=5, fill="x")

            # Eventos para cambiar el color del fondo al pasar el cursor
             label_cancion.bind("<Enter>", lambda event, lbl=label_cancion: lbl.config(bg="#d1e0ff"))
             label_cancion.bind("<Leave>", lambda event, lbl=label_cancion: lbl.config(bg="#ffffff"))

             label_cancion.bind("<Button-1>", lambda event, song_name=nombre: self.reproducir_cancion_desde_carpeta(song_name))

     except Exception as e:
         messagebox.showerror("Error", f"Error al cargar canciones del género: {e}")
     finally:
         cursor.close()
         conn.close()


    def play_pause_musica(self):
        if self.is_playing:
            pygame.mixer.music.pause()
            self.is_playing = False
            self.button_play_pause.config(text="Play")
        else:
            pygame.mixer.music.unpause()
            self.is_playing = True
            self.button_play_pause.config(text="Pause")

    def actualizar_tiempo(self):
        if self.is_playing and not self.slider_dragging:
            current_time = pygame.mixer.music.get_pos() / 1000
            self.scale.set(current_time)
            minutos_actuales = int(current_time // 60)
            segundos_actuales = int(current_time % 60)
            minutos_totales = int(self.track_length // 60)
            segundos_totales = int(self.track_length % 60)
            self.label_tiempo.config(text=f"{minutos_actuales:02}:{segundos_actuales:02} / {minutos_totales:02}:{segundos_totales:02}")
        self.root.after(1000, self.actualizar_tiempo)

    def actualizar_tiempo_slider(self, event=None):
        current_time = float(self.scale.get())
        minutos_actuales = int(current_time // 60)
        segundos_actuales = int(current_time % 60)
        minutos_totales = int(self.track_length // 60)
        segundos_totales = int(self.track_length % 60)
        self.label_tiempo.config(text=f"{minutos_actuales:02}:{segundos_actuales:02} / {minutos_totales:02}:{segundos_totales:02}")

    def empezar_arrastrar_slider(self, event):
        self.slider_dragging = True

    def soltar_slider(self, event):
        new_pos = self.scale.get()
        
        pygame.mixer.music.play(start=new_pos)
        self.is_playing = True
        self.slider_dragging = False
        self.actualizar_tiempo_slider()

    def siguiente_musica(self):
        if self.current_playlist:
            self.current_track_index = (self.current_track_index + 1) % len(self.current_playlist)
            self.reproducir_cancion_desde_carpeta(self.current_playlist[self.current_track_index])

    def anterior_musica(self):
        if self.current_playlist:
            self.current_track_index = (self.current_track_index - 1) % len(self.current_playlist)
            self.reproducir_cancion_desde_carpeta(self.current_playlist[self.current_track_index])
            
    def guardar_estado_musica(self):
        estado = {
            "current_track_index": self.current_track_index,
            "current_time": pygame.mixer.music.get_pos() / 1000
        }
        with open("estado_musica.json", "w") as archivo:
            json.dump(estado, archivo)

    def cargar_estado_musica(self):
        try:
            with open("estado_musica.json", "r") as archivo:
                estado = json.load(archivo)
                self.current_track_index = estado.get("current_track_index", 0)
                self.current_time = estado.get("current_time", 0)
                return True
        except FileNotFoundError:
            return False

    def reproducir_ultima_musica(self):
        if self.cargar_estado_musica():
            self.reproducir_cancion_desde_carpeta(self.current_playlist[self.current_track_index], self.current_time)
        else:
            self.reproducir_cancion_desde_carpeta(self.current_playlist[self.current_track_index])


if __name__ == "__main__":
    root = tk.Tk()
    app = Mi_Consola(root)
    root.mainloop()