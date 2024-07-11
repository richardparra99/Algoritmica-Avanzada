class Usuario:
    def __init__(self, id_usuario, nombre, contrasena, correo, dispositivos, fecha_registro):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.contrasena = contrasena
        self.correo = correo
        self.dispositivos = dispositivos
        self.fecha_registro = fecha_registro

    def crear_usuario(self, id_usuario, nombre, contrasena, correo, dispositivos, fecha_registro):
        usuario = Usuario(id_usuario, nombre, contrasena, correo, dispositivos, fecha_registro)
        self.usuarios.append(usuario)
        return usuario