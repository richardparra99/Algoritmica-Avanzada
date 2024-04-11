import pandas as pd
import numpy as np

nombre = ['Empleado' + str(1) for i in range(1, 11)]
salario = np.random.uniform(2360, 5000, 10)
antiguedad = np.random.randint(1 , 10, 10)
cargos = np.random.choice(['Gerente', 'Frontend', 'Backend', 'Devops', 'Designer'], 10)

df = pd.DataFrame({
    'Nombre': nombre,
    'Salario': salario,
    'Antiguedad': antiguedad,
    'Cargos': cargos
})
# print(df)

df_youtube = pd.read_csv('Panda/Most Subscribed YouTube Channels_exported.csv', sep=",", header=0)
print(df_youtube.head(10)) # devuelve los primeros 5
names = df_youtube["Name"]
print(names)
# menos Suscripciones
subscrubers_min = df_youtube["Subscribers (millions)"].min()
print(subscrubers_min)
print(df_youtube.tail()[["Name","Subscribers (millions)"]])

subscribers_max = df_youtube["Subscribers (millions)"].idxmax()

# Obtiene el nombre del canal con más suscriptores
channel_name = df_youtube.loc[subscribers_max, "Name"]

print("Canal con más suscriptores:", channel_name)

print(df_youtube[11:21]["Category"])

max_value = df_youtube["Subscribers (millions)"].max()
subscribers_max_row = df_youtube[df_youtube["Subscribers (millions)"] == max_value]
channel_name = subscribers_max_row["name"]
print(channel_name)