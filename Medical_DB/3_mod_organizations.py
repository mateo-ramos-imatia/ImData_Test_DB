import pandas as pd
import numpy as np

'''
Modifica organizations.csv, para dividirlo en 3 tablas 1,2,3
Se reparten las organizaciones originales
Cada tabla tiene unas columnas diferentes (con solapamiento)
Hay también solapamiento de filas
Por tanto hay entradas que solo estarán en una tabla, habrá otras duplicadas entre tablas
'''

# Cargar el CSV original
df = pd.read_csv('csvs/_organizations.csv')
for col in df.select_dtypes(include='float'):
    # Verificamos si todos los valores no nulos son enteros
    if df[col].dropna().apply(float.is_integer).all():
        df[col] = df[col].astype('Int64')


# Mezclar aleatoriamente las filas
df_shuffled = df.sample(frac=1, random_state=42).reset_index(drop=True)

# Calcular número de filas a seleccionar (~60%)
n = len(df)

# Obtener índices aleatorios únicos para cada grupo
indices = np.arange(n)
np.random.seed(42)

indices1_10 = np.random.choice(indices, size=int(n*0.1), replace=False)
indices = np.setdiff1d(indices, indices1_10)

indices2_10 = np.random.choice(indices, size=int(n*0.1), replace=False)
indices = np.setdiff1d(indices, indices2_10)

indices3_10 = np.random.choice(indices, size=int(n*0.1), replace=False)
indices = np.random.permutation(np.setdiff1d(indices, indices3_10))

indices_remaining_123 = np.array_split(indices, 3)

indices_repeated_1 = np.random.choice(indices, size=int(n*0.3), replace=False)
indices_repeated_2 = np.random.choice(indices, size=int(n*0.3), replace=False)
indices_repeated_3 = np.random.choice(indices, size=int(n*0.3), replace=False)

indices1 = np.unique(np.concatenate([indices1_10, indices_remaining_123[0], indices_repeated_1]))
indices2 = np.unique(np.concatenate([indices2_10, indices_remaining_123[1], indices_repeated_2]))
indices3 = np.unique(np.concatenate([indices3_10, indices_remaining_123[2], indices_repeated_3]))

# Crear los tres DataFrames
df1 = df.loc[indices1, ['Id', 'NAME', 'ADDRESS', 'CITY', 'STATE', 'ZIP']]
df2 = df.loc[indices2, ['Id', 'NAME', 'LAT', 'LON']]
df3 = df.loc[indices3, ['Id', 'LAT', 'LON', 'PHONE', 'REVENUE', 'UTILIZATION']]

# Guardar los nuevos CSVs
df1.to_csv('csvs/_organizations_F1.csv', index=False)
df2.to_csv('csvs/_organizations_F2.csv', index=False)
df3.to_csv('csvs/_organizations_F3.csv', index=False)

print("Archivos generados: _organizations_F1.csv, _organizations_F2.csv, _organizations_F3.csv")



# Cargar los CSVs
df1 = pd.read_csv('csvs/_organizations_F1.csv')
df2 = pd.read_csv('csvs/_organizations_F2.csv')
df3 = pd.read_csv('csvs/_organizations_F3.csv')

# Extraer IDs únicos de cada CSV
ids1 = set(df1['Id'].dropna())
ids2 = set(df2['Id'].dropna())
ids3 = set(df3['Id'].dropna())

# 1. Cantidad de IDs únicos en cada CSV
unique_1 = len(ids1)
unique_2 = len(ids2)
unique_3 = len(ids3)

# 2. Total de IDs únicos entre los tres CSVs
total_unique = len(ids1 | ids2 | ids3)

# 3. Repeticiones en cada CSV con respecto a los otros
repeated_1 = len(ids1 & (ids2 | ids3))
repeated_2 = len(ids2 & (ids1 | ids3))
repeated_3 = len(ids3 & (ids1 | ids2))

# Mostrar resultados
print(f"IDs únicos en _organizations_F1.csv: {unique_1}")
print(f"IDs únicos en _organizations_F2.csv: {unique_2}")
print(f"IDs únicos en _organizations_F3.csv: {unique_3}")
print(f"Total de IDs únicos entre los tres CSVs: {total_unique}")
print(f"IDs de _organizations_F1.csv también presentes en otros CSVs: {repeated_1}")
print(f"IDs de _organizations_F2.csv también presentes en otros CSVs: {repeated_2}")
print(f"IDs de _organizations_F3.csv también presentes en otros CSVs: {repeated_3}")
