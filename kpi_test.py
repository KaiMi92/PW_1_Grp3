import pandas as pd

df = pd.read_csv('drivedata.csv')

if 'Time' not in df.columns:
    raise ValueError('Die Spalte Zeit wurde nicht in der CSV Datei gefunden')

# Differenz berechnen
df['Differenz'] = df['Time'].diff()

print(df)