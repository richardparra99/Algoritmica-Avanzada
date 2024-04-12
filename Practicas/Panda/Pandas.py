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

#max_value = df_youtube["Subscribers (millions)"].max()
#subscribers_max_row = df_youtube[df_youtube["Subscribers (millions)"] == max_value]
#channel_name = subscribers_max_row["name"]
#print(channel_name)

# cambiar los nombres en español utilizando pandas
# Definir un diccionario con los nombres de columnas en español
nombres_espanol_pais = {
    "Name": "Nombre",
    "Brand channel": "Canal de marca",
    "Subscribers (millions)": "Suscriptores (millones)",
    "Primary language": "Lenguaje primaria",
    "Category": "Categoria",
    "Country": "País/Región"
}

# Renombrar las columnas utilizando el diccionario
df_youtube = df_youtube.rename(columns=nombres_espanol_pais)

# Mapear los valores de las filas al español
mapeo_filas = {
    "United States": "Estados Unidos",
    "India": "India",
    "Ukraine- United States": "Ucrania - Estados Unidos",
    "Russia- United States": "Rusia- Estados Unidos",
    "Sweden": "Suecia",
    "South Korea": "Corea Sur",
    "Cyprus[a]": "Chipre",
    "Brazil": "Brasil",
    "United Kingdom": "Reino Unido",
    "United States ( Puerto Rico)": "Estados Unidos (Puerto Rico)",
    "Belarus": "Bielorussia",
    "Pakistan": "Pakistán",
    "Romania": "Rumania"
}
df_youtube = df_youtube.replace({"País/Región": mapeo_filas})

# Mostrar el DataFrame con los nombres de las columnas en español


mapeo_filas = {
    "Music": "Música",
    "Education": "Educacion",
    "Entertainment": "Entretenimiento",
    "Sports": "Deporte",
    "Film": "Peliculas",
    "News": "Noticias",
    "How-to": "Como Hacer",
    "Games": "Juegos"
} 
nombre_lenguaje_primaria = {
    "Hindi[7][8]": "Hindi",
    "English": "Ingles",
    "English[10][11][12]": "Ingles",
    "Korean": "Coreano",
    "Portuguese": "Portugues",
    "Russian": "Rusia",
    "UrdU": "Lashkari",
    "Spanish": "Español",
    "Hindi[9]": "Hindi",
    "Hindi[16]": "Hindi",
    "Hindi[13][14]": "Hindi",
    "Bhojpuri": "Grupo etnolinguistico",
    "Urdu": "Campamento"
}
nombre_canal = {
    "Yes": "Si"
}

# Supongamos que quieres agregar una nueva fila con estos datos
nueva_fila = pd.DataFrame({
    "Nombre": ["Medusa"],
    "Canal de marca": ["No"],
    "Suscriptores (millones)": [5.6],
    "Lenguaje primaria": ["Español"],
    "Categoria": ["Musica"],
    "País/Región": ["Bolivia"]
})

# Concatenar el DataFrame de la nueva fila con df_youtube
df_youtube = pd.concat([df_youtube, nueva_fila], ignore_index=True)

print("DataFrame con la nueva fila:")
print(df_youtube.tail()) 
# Supongamos que deseas eliminar la fila con índice 5
#indice_a_eliminar = 50

# Eliminar la fila del DataFrame
#df_youtube = df_youtube.drop(indice_a_eliminar)

#print("DataFrame después de eliminar la fila:")
#print(df_youtube.tail()) 

# Convertir los valores de las categorías a minúsculas antes de realizar el reemplazo
df_youtube["Canal de marca"] = df_youtube["Canal de marca"].str.capitalize()
df_youtube = df_youtube.replace({"Canal de marca": nombre_canal})

df_youtube["Lenguaje primaria"] = df_youtube["Lenguaje primaria"].str.capitalize()
df_youtube = df_youtube.replace({"Lenguaje primaria": nombre_lenguaje_primaria})

df_youtube["Categoria"] = df_youtube["Categoria"].str.capitalize()
df_youtube = df_youtube.replace({"Categoria": mapeo_filas})
print(df_youtube)