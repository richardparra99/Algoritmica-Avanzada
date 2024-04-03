# esto es un comentario en linea
"""dentro de las 3 comillas puedo comentar varias lineas de codigo"""

'''tambien puedo usar comillas simples'''

saludo = "hola mundo!"
edad = 32
edad = False

print("Edad es de tipo", type(edad))
print(len(saludo)) # len() es un metodo incorporado
print(saludo)

listas = [1, 2, 3]
tuplas = (1, 2, 3)

# Operadores en pyhton
# Operadores arimeticos
resultado = 5 // 5
print(resultado)
print(type(resultado))
mult = 5.2 * 5
print(mult)

numero = 25
if numero > 25:
    print("es mayor a 25")
elif numero < 2:
    print("es menor a 5")
else:
    print("lo que se")

nombre = "Eduardo"
edad = 32
mensaje = "Mi nombre es " + nombre + " y tengo " + str(edad)
mensaje2 = "Mi nombre es ", nombre, " y tengo ", str(edad)
print(mensaje2)
print(mensaje)





