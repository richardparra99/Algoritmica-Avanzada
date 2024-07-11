import tkinter as tk
import random
import time

def quicksort(arr):
    if len(arr) <= 1:
        return arr
    else:
        pivote = arr[0]
        menor = [x for x in arr[1:] if x <= pivote]
        mayor = [x for x in arr[1:] if x > pivote]
        return quicksort(menor) + [pivote] + quicksort(mayor)

def draw_histogram(canvas, data):
    canvas.delete("all")
    ancho = 20
    escala_altura = 10
    for i, value in enumerate(data):
        x0 = i * 30 + 50
        y0 = 300
        x1 = x0 + ancho
        y1 = y0 - value * escala_altura
        canvas.create_rectangle(x0, y0, x1, y1, fill="black")
        canvas.create_text((x0 + x1) / 2, y0 + 10, text=str(value))

def ordenar_histograma():
    global data
    datos_ordenados = quicksort(data)
    animar_clasificar(datos_ordenados, 0)

def animar_clasificar(datos_ordenado, index):
    if index < len(datos_ordenado):
        draw_histogram(canvas, datos_ordenado[:index] + [datos_ordenado[index]] + data[index + 1:])
        canvas.update()
        time.sleep(0.1)  # Ajusta el tiempo de pausa
        animar_clasificar(datos_ordenado, index + 1)
    else:
        draw_histogram(canvas, datos_ordenado)
        canvas.update()

def generate_histograma():
    global data
    data = [random.randint(1, 20) for _ in range(15)]
    draw_histogram(canvas, data)

# Crear ventana
root = tk.Tk()
root.title("Ordenador de Histograma con Quicksort")

# Crear lienzo
canvas = tk.Canvas(root, width=600, height=400)
canvas.pack()

# Botones
generate_button = tk.Button(root, text="Generar Histograma", command=generate_histograma)
generate_button.pack(side=tk.LEFT, padx=10)
sort_button = tk.Button(root, text="Ordenar Histograma", command=ordenar_histograma)
sort_button.pack(side=tk.LEFT, padx=10)

# Generar histograma inicial
generate_histograma()

# Iniciar bucle de la interfaz gráfica
root.mainloop()
