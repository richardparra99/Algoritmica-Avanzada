import numpy as np

scalar = np.array(50)
print(scalar)
print(scalar.ndim)

#Vector
vector = np.array([1,5,3,8])
print(vector)
print(vector.ndim)

#Matriz
matriz = np.array([[5,3,1],[2,1,3]])
print(matriz)
print(matriz.ndim)

#Matriz 3 dimensiones
matriz3 = np.array([ [[1,2,3],[4,5,6], [7,8,9]],
[[10,11,12],[13,14,15],[16,17,18]],
[[19,20,21],[22,23,24],[25,26,27]]
])
print(matriz3)
print(matriz3.ndim)

# rango
print("=== RANGO ===")
lista = list(range(1, 11))
print(lista)

# arrange
print("=== ARANGE ===")
listaNp = np.arange(1, 30)
print(listaNp)

#Zero
print("=== ZERO ===")
listaZero = np.zeros(10)
print(listaZero)
print(np.zeros((10, 10)))

#Unos
print("=== UNOS ===")
ListaUno = np.ones(5)
print(ListaUno)
print(np.ones((10, 10)))

#EYE
print("=== EYE ===")
eyeMatriz = np.eye(5)
inverso = eyeMatriz[::-1]
print(eyeMatriz)
print(inverso)

# Numero Random
print("=== Numero Ramdom ===")
print(np.random.rand())
matrizRandom = np.random.rand(2, 2)
print(matrizRandom)

# Numero Enteros
print("=== Numero Enteros ===")
print(np.random.randint(1, 5))
print(np.random.randint(1, 5, (10, 10)))

# Condicionales
print("=== Condicionales ===")
print(listaNp[listaNp > 25])
print(listaNp[(listaNp %2 == 0)])
print(listaNp[(listaNp > 10) & (listaNp > 20)])

datos = np.random.randint(1, 5, 10)
print("funciones en Numpy")
print(datos)
print(datos.max())
print(datos.argmax())
print(datos.min())
print(datos.argmin())
datos.sort()
print("media: ", datos.mean())
median = np.median(datos)
medianRounded = np.round(median)
print("Mediana: " + str(median))
print("Mediana Redondeada: " + str(medianRounded))
print(np.percentile(datos, 50))
print(np.var(datos)) # varianza
print(np.std(datos))
