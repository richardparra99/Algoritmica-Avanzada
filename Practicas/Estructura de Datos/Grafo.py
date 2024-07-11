class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.conexiones = []

    def agregar_conexion(self, nodo, peso=1):
        self.conexiones.append(nodo)


class Grafo:
    def __init__(self):
        self.nodos = {}

    def agregar_nodo(self, valor):
        nuevo_nodo = Nodo(valor)
        self.nodos[valor] = nuevo_nodo

    def agregar_conexiones(self, desde, hacia, peso=1):
        if desde not in self.nodos:
            self.agregar_nodo(desde)
        if hacia not in self.nodos:
            self.agregar_nodo(hacia)
        self.nodos[desde].agregar_conexion(self.nodos[hacia], peso)

    def obtener_nodo(self, valor):
        return self.nodos.get(valor)


# Recorrido en profundidad (DFS) pre-orden
def preorden(nodo, visitados=None):
    if visitados is None:
        visitados = set()
    visitados.add(nodo.valor)
    print(nodo.valor, end = " - ")
    for conexion in nodo.conexiones:
        if conexion.valor not in visitados:
            preorden(conexion, visitados)


# Recorrido en profundidad (DFS) in-orden
def inorden(nodo, visitados=None):
    if visitados is None:
        visitados = set()
    visitados.add(nodo.valor)
    if len(nodo.conexiones) >= 2:
        inorden(nodo.conexiones[0], visitados)  # Recorrido del subárbol izquierdo
        print(nodo.valor, end = " - ")  # Visita del nodo raíz
        inorden(nodo.conexiones[1], visitados)  # Recorrido del subárbol derecho
    elif len(nodo.conexiones) == 1:
        inorden(nodo.conexiones[0], visitados)  # Caso especial de solo un hijo izquierdo
        print(nodo.valor, end = " - ")
    else:
        print(nodo.valor, end = " - ")  # Caso base de nodo hoja


# Recorrido en profundidad (DFS) post-orden
def postorden(nodo, visitados=None):
    if visitados is None:
        visitados = set()
    visitados.add(nodo.valor)
    for conexion in nodo.conexiones:
        if conexion.valor not in visitados:
            postorden(conexion, visitados)
    print(nodo.valor, end = " - ")


# Crear un grafo de ejemplo
grafo = Grafo()
grafo.agregar_conexiones('A', 'B')
grafo.agregar_conexiones('A', 'C')
grafo.agregar_conexiones('B', 'D')
grafo.agregar_conexiones('B', 'E')
grafo.agregar_conexiones('C', 'F')
grafo.agregar_conexiones('C', 'G')

# Recorrer el grafo en profundidad pre-orden
print("Recorrido en profundidad pre-orden:")
nodo_inicial = grafo.obtener_nodo('A')
preorden(nodo_inicial)

# Recorrer el grafo en profundidad in-orden
print("\nRecorrido en profundidad in-orden:")
nodo_inicial = grafo.obtener_nodo('A')
inorden(nodo_inicial)

# Recorrer el grafo en profundidad post-orden
print("\nRecorrido en profundidad post-orden:")
nodo_inicial = grafo.obtener_nodo('A')
postorden(nodo_inicial)
