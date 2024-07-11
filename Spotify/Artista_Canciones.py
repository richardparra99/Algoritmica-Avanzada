import pandas as pd

df_spotify = pd.read_csv('C:/Users/Richard-P/Algoritmica-Avanzada/Spotify/Spotify_Youtube.csv', sep=",", header=0)

# print(df_spotify.head(30))
print(df_spotify.tail())
# print(df_spotify.iloc())
# print(df_spotify.shape)