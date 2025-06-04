import pandas as pd
import uuid
import random

'''
Creación de nuevos encounters correspondientes a las hospital_admisions_A/B. No existían
Estas hospital_admisions se refieren a los pacientes en _Patients_3.csv
'''




def corregir_float(df):
    for col in df.select_dtypes(include='float'):
        # Verificamos si todos los valores no nulos son enteros
        if df[col].dropna().apply(float.is_integer).all():
            df[col] = df[col].astype('Int64')
    return df

# Ruta al archivo original
archivo_original = 'csvs/_hospital_admisions_A.csv'

# Leer el archivo separado por tabulaciones
df_ha_dates = pd.read_csv('csvs/_hospital_admisions_A.csv', delimiter='\t')
df_ha_dates = corregir_float(df_ha_dates)
df_ha_info = pd.read_csv('csvs/_hospital_admisions_B.csv', delimiter='\t')
df_ha_info = corregir_float(df_ha_info)

# Reemplazar comas en la columna 'PrimaryDiagnosisDescription'
df_ha_info['PrimaryDiagnosisDescription'] = df_ha_info['PrimaryDiagnosisDescription'].str.replace(',', '', regex=False)

df_ha = pd.merge(df_ha_dates, df_ha_info, on=['PatientID', 'AdmissionID'], how='inner')



################## ORGANIZATIONS
df_org = pd.read_csv('csvs/_organizations.csv')
df_org = corregir_float(df_org)

# Filtrar las filas donde 'NAME' contiene 'HOSPITAL' (ignorando mayúsculas)
filtro_hospital = df_org['NAME'].str.contains('HOSPITAL', case=False, na=False)

# Extraer los valores de la columna 'Id' correspondientes
ids_hospital = df_org.loc[filtro_hospital, 'Id'].tolist()

################### PROVIDERS
df_prov = pd.read_csv('csvs/_providers.csv')
df_prov = corregir_float(df_prov)

# Crear el diccionario
hospital_providers = {}

for hosp_id in ids_hospital:
    # Filtrar providers donde 'ORGANIZATION' coincide con el ID del hospital
    matching_providers = df_prov[df_prov['ORGANIZATION'] == hosp_id]

    # Obtener los nombres de los providers (puedes cambiar la columna si no es 'NAME')
    providers_list = matching_providers['Id'].dropna().tolist()

    # Guardar en el diccionario
    hospital_providers[hosp_id] = providers_list


################## CREATE ENCOUNTERS
columnas_encounters = [
    "Id", "START", "STOP", "PATIENT", "ORGANIZATION", "PROVIDER", "PAYER",
    "ENCOUNTERCLASS", "ENCOUNTER_SNOMED_CODE", "DESCRIPTION",
    "BASE_ENCOUNTER_COST", "TOTAL_CLAIM_COST", "PAYER_COVERAGE",
    "REASON_SNOMED_CODE", "REASONDESCRIPTION"
]

# Crear DataFrame vacío
df_encuentros = pd.DataFrame(columns=columnas_encounters)

for index, row in df_ha.iterrows():
    org = random.choice(ids_hospital)
    nueva_fila = {
        "Id": uuid.uuid4(),
        "START": None,
        "STOP": None,
        "PATIENT": row["PatientID"],
        "ORGANIZATION": org ,
        "PROVIDER": random.choice(hospital_providers[org]),
        "PAYER": None,
        "ENCOUNTERCLASS": "emergency",
        "ENCOUNTER_SNOMED_CODE": 50849002,
        "DESCRIPTION": row['PrimaryDiagnosisDescription'],
        "BASE_ENCOUNTER_COST": None,
        "TOTAL_CLAIM_COST": None,
        "PAYER_COVERAGE": None,
        "REASON_SNOMED_CODE": None,
        "REASONDESCRIPTION": None
    }

    matching_row = df_ha_dates[(df_ha_dates['PatientID'] == row['PatientID']) &
                               (df_ha_dates['AdmissionID'] == row['AdmissionID'])]

    df_ha_dates.loc[matching_row.index, 'encounter'] = nueva_fila['Id']
    df_ha_dates.loc[matching_row.index, 'organization'] = org


    df_encuentros.loc[len(df_encuentros)] = nueva_fila

df_encuentros = df_encuentros.drop(columns=['PAYER'])



# Guardar una copia separada por comas
df_ha_dates.to_csv('csvs/_hospital_admisions_F1.csv', index=False)
df_ha_info.to_csv('csvs/_hospital_admisions_F2.csv', index=False)

df_encuentros.to_csv('csvs/_encounters_F2.csv', index=False)

