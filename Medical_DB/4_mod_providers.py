import pandas as pd
import numpy as np
import re


'''
Dividir todos los providers en 2 tablas. 
No se mantienen todas las variables para cada tabla, solo algunas

'''

# Mostrar todas las columnas
pd.set_option('display.max_columns', None)

# Mostrar todas las filas (si también quieres eso)
pd.set_option('display.max_rows', None)

# Evitar que corte el contenido de columnas anchas
pd.set_option('display.max_colwidth', None)

# Evitar que se trunque el DataFrame en horizontal
pd.set_option('display.expand_frame_repr', False)





def limpiar_nombre(nombre_completo):
    # Dividir en nombre y apellido
    partes = nombre_completo.split()
    # Usar expresión regular para quitar los números al final de cada parte
    partes_limpias = [re.sub(r'\d+$', '', parte) for parte in partes]
    # Unir las partes limpias en un solo string
    return ' '.join(partes_limpias)


# Cargar el CSV original
df = pd.read_csv('csvs/_providers.csv')

for col in df.select_dtypes(include='float'):
    # Verificamos si todos los valores no nulos son enteros
    if df[col].dropna().apply(float.is_integer).all():
        df[col] = df[col].astype('Int64')

#arreglar nombres quitando numeros
df['NAME'] = df['NAME'].apply(limpiar_nombre)

####################
# df['temp'] = df['NAME'] + df['ORGANIZATION']
#
# nombres_repetidos = df['temp'].value_counts()
# nombres_repetidos = nombres_repetidos[nombres_repetidos > 1].index
# # Filtrar el DataFrame completo por esos nombres
# filas_duplicadas = df[df['temp'].isin(nombres_repetidos)]
#
# print(filas_duplicadas)
##################

# Mezclar aleatoriamente las filas
df_shuffled = df.sample(frac=1, random_state=42).reset_index(drop=True)

# Calcular número de filas
n = len(df)

# Obtener índices aleatorios únicos para cada grupo
indices = np.arange(n)
np.random.seed(42)

indices2 = np.random.choice(indices, size=int(n*0.3), replace=False)

# Crear los  DataFrames
df1 = df.loc[indices, ['Id','ORGANIZATION','NAME','GENDER','ADDRESS','CITY','STATE','ZIP']]
df2 = df.loc[indices2, ['Id', 'NAME','GENDER',  'LAT', 'LON','SPECIALITY','UTILIZATION']]

# Guardar los nuevos CSVs
df1.to_csv('csvs/_providers_F1.csv', index=False)
df2.to_csv('csvs/_providers_F2.csv', index=False)



