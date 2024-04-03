class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.conexiones = {}  # Un diccionario para almacenar las conexiones
        self.visitado = False  # Para el recorrido del árbol
