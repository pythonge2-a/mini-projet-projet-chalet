# lecture du fichier d'input 
import pandas as pd

file_path = 'data/simulated_weather_data.csv'
df = pd.read_csv(file_path)

last_row = df.tail(1)
print(last_row)
