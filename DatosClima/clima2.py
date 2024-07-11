import tkinter as tk
from tkinter import messagebox
import requests
import matplotlib.pyplot as plt
import mplcursors
from datetime import datetime, timedelta
import csv
import pandas as pd
from tkinter import ttk
from sklearn.linear_model import LinearRegression
import numpy as np

def train_model():
    # Datos históricos ficticios: debes reemplazar esto con tus propios datos
    data = {
        'humidity': [50, 60, 70, 80, 90, 40, 30, 20, 10, 80, 60, 70],
        'wind_speed': [5, 6, 7, 8, 9, 4, 3, 2, 1, 8, 6, 7],
        'pressure': [1012, 1013, 1014, 1015, 1016, 1011, 1010, 1009, 1008, 1015, 1013, 1014],
        'temperature': [20, 21, 22, 23, 24, 19, 18, 17, 16, 23, 21, 22]
    }
    df = pd.DataFrame(data)
    
    X = df[['humidity', 'wind_speed', 'pressure']]
    y = df['temperature']
    
    model = LinearRegression()
    model.fit(X, y)
    
    return model

model = train_model()

def predict_temperature(humidity, wind_speed, pressure):
    new_data = np.array([[humidity, wind_speed, pressure]])
    return model.predict(new_data)[0]

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
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']

        # Predicción de la temperatura futura
        predicted_temp = predict_temperature(humidity, wind_speed, pressure)

        result_text = (f"Temperatura: {temp} °C\n"
                       f"Velocidad del viento: {wind_speed} m/s\n"
                       f"Latitud: {latitude}\n"
                       f"Longitud: {longitude}\n"
                       f"Descripción del clima: {description}\n"
                       f"Predicción de temperatura futura: {predicted_temp:.2f} °C")
        result_label.config(text=result_text)

        get_forecast(city, api_key)

    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"No se pudo obtener los datos del clima: {e}")
    except KeyError:
        messagebox.showerror("Error", "Ciudad no encontrada, por favor ingrese una ciudad válida.")

def get_forecast(city, api_key):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric&cnt=40"
    try:
        res = requests.get(url)
        res.raise_for_status()
        data = res.json()

        forecast_data = []
        predicted_data = []
        for entry in data['list']:
            date = datetime.fromtimestamp(entry['dt'])
            temp = entry['main']['temp']
            wind_speed = entry['wind']['speed']
            description = entry['weather'][0]['description']
            humidity = entry['main']['humidity']
            pressure = entry['main']['pressure']

            # Predicción basada en los datos del pronóstico
            predicted_temp = predict_temperature(humidity, wind_speed, pressure)

            forecast_data.append((city, date, temp, wind_speed, description))
            predicted_data.append((city, date, predicted_temp, wind_speed, description))
            save_data(city, date, temp, wind_speed, description)

        plot_comparison(forecast_data, predicted_data, f'Comparación de temperatura real y predicha para {city}')

    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"No se pudo obtener los datos del pronóstico: {e}")

def save_data(city, date, temp, wind_speed, description):
    with open('weather_data.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([city, date, temp, wind_speed, description])

def plot_comparison(forecast_data, predicted_data, title):
    dates = [entry[1] for entry in forecast_data]
    temps_real = [entry[2] for entry in forecast_data]
    temps_pred = [entry[2] for entry in predicted_data]
    descriptions = [entry[4] for entry in forecast_data]

    plt.figure(figsize=(14, 7))
    plt.plot(dates, temps_real, marker='o', color='b', label='Temperatura Real')
    plt.plot(dates, temps_pred, marker='o', color='r', label='Temperatura Predicha')
    plt.title(title)
    plt.xlabel('Fecha')
    plt.ylabel('Temperatura (°C)')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()

    # Añadir interactividad con mplcursors
    cursor = mplcursors.cursor(hover=True)
    cursor.connect("add", lambda sel: sel.annotation.set_text(f"{dates[int(sel.index)]}\nReal: {temps_real[int(sel.index)]}°C\nPredicha: {temps_pred[int(sel.index)]}°C\n{descriptions[int(sel.index)]}"))

    plt.show()

def load_and_compare_weather_data():
    try:
        df = pd.read_csv('weather_data.csv', names=['City', 'Date', 'Temperature', 'Wind Speed', 'Description'])
        # Filtrar solo los datos de Santa Cruz
        sc_data = df[df['City'] == 'Santa Cruz']
        sc_data['Date'] = pd.to_datetime(sc_data['Date'])
        sc_data = sc_data.sort_values(by='Date')

        # Agrupar por fecha y calcular la media, máxima y mínima de la temperatura diaria
        sc_data['Date'] = sc_data['Date'].dt.date
        daily_stats = sc_data.groupby('Date')['Temperature'].agg(['mean', 'max', 'min']).reset_index()

        plt.figure(figsize=(14, 7))
        mean_plot, = plt.plot(daily_stats['Date'], daily_stats['mean'], marker='o', linestyle='-', color='b', label='Media')
        max_plot, = plt.plot(daily_stats['Date'], daily_stats['max'], marker='o', linestyle='-', color='r', label='Máxima')
        min_plot, = plt.plot(daily_stats['Date'], daily_stats['min'], marker='o', linestyle='-', color='g', label='Mínima')
        plt.fill_between(daily_stats['Date'], daily_stats['min'], daily_stats['max'], color='gray', alpha=0.2)
        plt.title('Temperaturas diarias promedio, máxima y mínima para Santa Cruz')
        plt.xlabel('Fecha')
        plt.ylabel('Temperatura (°C)')
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.legend()
        plt.tight_layout()

        # Añadir interactividad con mplcursors
        cursor = mplcursors.cursor([mean_plot, max_plot, min_plot], hover=True)
        cursor.connect("add", lambda sel: sel.annotation.set_text(
            f"{daily_stats['Date'].iloc[int(sel.index)]}: \n"
            f"Media: {daily_stats['mean'].iloc[int(sel.index)]:.2f}°C\n"
            f"Máxima: {daily_stats['max'].iloc[int(sel.index)]:.2f}°C\n"
            f"Mínima: {daily_stats['min'].iloc[int(sel.index)]::.2f}°C"
        ))

        plt.show()

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar los datos: {e}")

def mostrar_datos_csv_en_tabla():
    try:
        df = pd.read_csv('weather_data.csv', names=['City', 'Date', 'Temperature', 'Wind Speed', 'Description'])

        root = tk.Tk()
        root.title("Datos del Clima Registrados")

        tree = ttk.Treeview(root)
        tree['columns'] = list(df.columns)
        tree['show'] = 'headings'

        for column in df.columns:
            tree.heading(column, text=column)
            tree.column(column, anchor='center')

        for index, row in df.iterrows():
            tree.insert('', 'end', values=list(row))

        tree.pack(expand=True, fill='both')
        root.mainloop()

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar los datos: {e}")

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

compare_button = tk.Button(root, text="Comparar datos históricos", command=load_and_compare_weather_data)
compare_button.pack()

mostrar_csv_button = tk.Button(root, text="Mostrar datos registrados", command=mostrar_datos_csv_en_tabla)
mostrar_csv_button.pack()

# Iniciar el bucle principal de la interfaz
root.mainloop()