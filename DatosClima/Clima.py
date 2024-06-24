import tkinter as tk
from tkinter import messagebox
import requests
import matplotlib.pyplot as plt
from datetime import datetime

def get_weather():
    city = city_entry.get()
    api_key = "3e0a4bdc8985cb158b77c90782afcc6a"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:
        res = requests.get(url)
        res.raise_for_status()
        data = res.json()

        temp = data['main']['temp']
        wind_speed = data['wind']['speed']
        latitude = data['coord']['lat']
        longitude = data['coord']['lon']
        description = data['weather'][0]['description']

        result_text = (f"Temperatura: {temp} °C\n"
                       f"Velocidad del viento: {wind_speed} m/s\n"
                       f"Latitud: {latitude}\n"
                       f"Longitud: {longitude}\n"
                       f"Descripción del clima: {description}")

        result_label.config(text=result_text)

        get_forecast(city, api_key)

    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"No se pudo obtener los datos del clima: {e}")
    except KeyError:
        messagebox.showerror("Error", "Ciudad no encontrada, por favor ingrese una ciudad válida.")

def get_forecast(city, api_key):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"

    try:
        res = requests.get(url)
        res.raise_for_status()
        data = res.json()

        # Procesar datos para los próximos días
        dates = []
        temps = []
        for entry in data['list']:
            date = datetime.fromtimestamp(entry['dt'])
            dates.append(date)
            temps.append(entry['main']['temp'])

        plot_forecast(dates, temps)

    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"No se pudo obtener los datos del pronóstico: {e}")

def plot_forecast(dates, temps):
    plt.figure(figsize=(10, 5))
    plt.plot(dates, temps, marker='o', linestyle='-', color='b')
    plt.title('Pronóstico de temperatura para los próximos días')
    plt.xlabel('Fecha')
    plt.ylabel('Temperatura (°C)')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Crear la ventana principal
root = tk.Tk()
root.title("Consulta del Clima")

# Crear los widgets
city_label = tk.Label(root, text="Ingrese una ciudad:")
city_label.pack()

city_entry = tk.Entry(root)
city_entry.pack()

search_button = tk.Button(root, text="Buscar", command=get_weather)
search_button.pack()

result_label = tk.Label(root, text="", justify="left")
result_label.pack()

# Iniciar el bucle principal de la interfaz
root.mainloop()
