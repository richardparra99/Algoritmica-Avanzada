import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX

# Cargar los datos históricos desde el archivo CSV
file_path = 'C:/Users/Richard-P/Algoritmica-Avanzada/DatosClima/climaSantaCruzGestion2023.csv'
historical_data = pd.read_csv(file_path)

# Convertir la columna 'date' al formato de fecha tz-naive
historical_data['date'] = pd.to_datetime(historical_data['date'])
historical_data['date'] = historical_data['date'].dt.tz_localize(None)

# Excluir la columna 'weather' si existe
if 'weather' in historical_data.columns:
    historical_data = historical_data[['date', 'temperature']]

# Asegurarse de que el índice es un DatetimeIndex
historical_data.set_index('date', inplace=True)

# Entrenar el modelo ARIMA con los datos históricos
daily_data = historical_data.resample('D').mean()

# Ajustar el modelo ARIMA
arima_model = SARIMAX(daily_data['temperature'], order=(5, 1, 1), seasonal_order=(1, 1, 1, 12))
arima_result = arima_model.fit(disp=False)

# Generar predicciones para todo julio de 2024
future_dates = pd.date_range(start='2024-07-01', end='2024-07-31', freq='D')
arima_predictions = arima_result.get_forecast(steps=len(future_dates)).predicted_mean

# Crear un DataFrame con las predicciones
arima_predictions_df = pd.DataFrame({
    'date': future_dates,
    'predicted_temperature': arima_predictions
})

# Graficar las predicciones para todo el mes de julio de 2024
plt.figure(figsize=(12, 6))
plt.plot(arima_predictions_df['date'], arima_predictions_df['predicted_temperature'], label='Predicted Temperature', marker='o', color='orange')
plt.xlabel('Date')
plt.ylabel('Temperature (°C)')
plt.title('Predicted Temperature for July 2024 (ARIMA)')
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()