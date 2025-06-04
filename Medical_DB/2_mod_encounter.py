import pandas as pd

'''
Pequeña corrección en encounters.csv
'''

def corregir_float(df):
    for col in df.select_dtypes(include='float'):
        # Verificamos si todos los valores no nulos son enteros
        if df[col].dropna().apply(float.is_integer).all():
            df[col] = df[col].astype('Int64')
    return df


# Cargar el archivo original
df = pd.read_csv('csvs/_encounters.csv')
df = corregir_float(df)
df_modified = df.drop(columns=['PAYER'])
# Guardar el archivo modificado de tratamientos
df_modified.to_csv('csvs/_encounters_F1.csv', index=False)

