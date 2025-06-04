import pandas as pd

'''
A partir de treatments:of_patients, se crea un nuevo tabla de medicinas
'''

# Cargar el archivo original
df = pd.read_csv('csvs/_treatements_of_patients.csv')

for col in df.select_dtypes(include='float'):
    # Verificamos si todos los valores no nulos son enteros
    if df[col].dropna().apply(float.is_integer).all():
        df[col] = df[col].astype('Int64')


# Crear el DataFrame de medicamentos sin duplicados
medicines_df = df[['RXCUI_CODE', 'DESCRIPTION']].drop_duplicates()

# Guardar el nuevo archivo de medicamentos
medicines_df.to_csv('csvs/_medicines_F1.csv', index=False)

# Eliminar las columnas que se movieron (excepto RXCUI_CODE, que se mantiene)
df_modified = df.drop(columns=['PAYER', 'DESCRIPTION'])




# Guardar el archivo modificado de tratamientos
df_modified.to_csv('_treatements_of_patients_F1.csv', index=False)

print("Archivos guardados: _medicines.csv y _treatements_of_patients.csv")
