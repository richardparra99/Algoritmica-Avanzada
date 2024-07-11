import tkinter as tk
from tkinter import messagebox
import requests
import matplotlib.pyplot as plt
import mplcursors
from datetime import datetime
import pandas as pd
from tkinter import ttk
from sklearn.preprocessing import LabelEncoder, StandardScaler, PolynomialFeatures
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import GridSearchCV
import numpy as np

# Función para cargar y preprocesar los datos del CSV
def preprocess_data():
    # Cargar el dataset
    df = pd.read_csv('C:/Users/Richard-P/Algoritmica-Avanzada/DatosClima/climaSantaCruzGestion2023.csv')

    # Convertir la columna 'weather' a valores numéricos
    le = LabelEncoder()
    df['weather'] = le.fit_transform(df['weather'])

    # Crear características polinómicas
    poly = PolynomialFeatures(degree=2, include_bias=False)
    poly_features = poly.fit_transform(df[['wind.speed', 'weather']])

    # Aplicar StandardScaler a las características polinómicas
    scaler = StandardScaler()
    poly_features_scaled = scaler.fit_transform(poly_features)

    # Convertir la columna 'date' a datetime
    df['date'] = pd.to_datetime(df['date'])

    return df, le, scaler, poly, poly_features_scaled

df, le, scaler, poly, poly_features_scaled = preprocess_data()

# Función para entrenar el modelo
def train_model():
    y = df['temperature']
    
    # Realizar búsqueda de hiperparámetros con GridSearchCV
    param_grid = {'n_neighbors': range(1, 31)}
    knn = KNeighborsRegressor()
    grid_search = GridSearchCV(knn, param_grid, cv=5, scoring='r2')
    grid_search.fit(poly_features_scaled, y)
    
    model = grid_search.best_estimator_
    return model

model = train_model()

# Función para predecir la temperatura
def predict_temperature(wind_speed, weather):
    new_data = np.array([[wind_speed, weather]])
    new_data_poly = poly.transform(new_data)
    new_data_scaled = scaler.transform(new_data_poly)
    return model.predict(new_data_scaled)[0]

# Función para agregar nuevas etiquetas al LabelEncoder
def add_new_labels(le, new_labels):
    classes = list(le.classes_)
    for label in new_labels:
        if label not in classes:
            classes.append(label)
    le.classes_ = np.array(classes)

# Función para obtener el clima actual usando la API
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

        if description not in le.classes_:
            add_new_labels(le, [description])
            weather_encoded = le.transform([description])[0]
        else:
            weather_encoded = le.transform([description])[0]

        # Predicción de la temperatura futura
        predicted_temp = predict_temperature(wind_speed, weather_encoded)

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

# Función para obtener el pronóstico usando la API
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

            if description not in le.classes_:
                add_new_labels(le, [description])
                weather_encoded = le.transform([description])[0]
            else:
                weather_encoded = le.transform([description])[0]

            # Predicción basada en los datos del pronóstico
            predicted_temp = predict_temperature(wind_speed, weather_encoded)

            forecast_data.append((city, date, temp, wind_speed, description))
            predicted_data.append((city, date, predicted_temp, wind_speed, description))

        plot_comparison(forecast_data, predicted_data, f'Comparación de temperatura real y predicha para {city}')
        calculate_metrics(forecast_data, predicted_data)

    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"No se pudo obtener los datos del pronóstico: {e}")

# Función para calcular el MAE y el R^2 del modelo
def calculate_metrics(forecast_data, predicted_data):
    real_temps = [entry[2] for entry in forecast_data]
    predicted_temps = [entry[2] for entry in predicted_data]

    mae = mean_absolute_error(real_temps, predicted_temps)
    r2 = r2_score(real_temps, predicted_temps)

    messagebox.showinfo("Métricas del modelo", f"MAE: {mae:.2f}\nR^2: {r2:.2f}")

# Función para graficar la comparación entre datos reales y predichos
def plot_comparison(forecast_data, predicted_data, title):
    dates = [entry[1] for entry in forecast_data]
    temps_real = [entry[2] for entry in forecast_data]
    temps_pred = [entry[2] for entry in predicted_data]

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
    cursor.connect("add", lambda sel: sel.annotation.set_text(f"{dates[int(sel.index)]}\nReal: {temps_real[int(sel.index)]}°C\nPredicha: {temps_pred[int(sel.index)]}°C"))

    plt.show()

# Función para cargar y comparar datos históricos
def load_and_compare_weather_data():
    try:
        df = pd.read_csv('C:/Users/Richard-P/Algoritmica-Avanzada/DatosClima/climaSantaCruzGestion2023.csv')
        df['date'] = pd.to_datetime(df['date'])
        sc_data = df[df['date'] > '2023-01-01']

        # Agrupar por fecha y calcular la media, máxima y mínima de la temperatura diaria
        sc_data['date'] = sc_data['date'].dt.date
        daily_stats = sc_data.groupby('date')['temperature'].agg(['mean', 'max', 'min']).reset_index()

        plt.figure(figsize=(14, 7))
        mean_plot, = plt.plot(daily_stats['date'], daily_stats['mean'], marker='o', linestyle='-', color='b', label='Media')
        max_plot, = plt.plot(daily_stats['date'], daily_stats['max'], marker='o', linestyle='-', color='r', label='Máxima')
        min_plot, = plt.plot(daily_stats['date'], daily_stats['min'], marker='o', linestyle='-', color='g', label='Mínima')
        plt.fill_between(daily_stats['date'], daily_stats['min'], daily_stats['max'], color='gray', alpha=0.2)
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
            f"{daily_stats['date'].iloc[int(sel.index)]}: \n"
            f"Media: {daily_stats['mean'].iloc[int(sel.index)]:.2f}°C\n"
            f"Máxima: {daily_stats['max'].iloc[int(sel.index)]:.2f}°C\n"
            f"Mínima: {daily_stats['min'].iloc[int(sel.index)]:.2f}°C"
        ))

        plt.show()

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar los datos: {e}")

# Función para mostrar los datos en una tabla
def mostrar_datos_csv_en_tabla():
    try:
        df = pd.read_csv('C:/Users/Richard-P/Algoritmica-Avanzada/DatosClima/climaSantaCruzGestion2023.csv')

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