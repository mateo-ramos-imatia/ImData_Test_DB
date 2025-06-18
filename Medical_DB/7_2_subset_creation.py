import pandas as pd
import os

def corregir_float(df):
    for col in df.select_dtypes(include='float'):
        # Verificamos si todos los valores no nulos son enteros
        if df[col].dropna().apply(float.is_integer).all():
            df[col] = df[col].astype('Int64')
    return df

#Leemos los csvs de los que partimos
df_encounters = pd.read_csv('./csvs/_encounters.csv', delimiter = ',')
df_encounters = corregir_float(df_encounters)
df_devices = pd.read_csv('./csvs/_devices_.csv', delimiter = ',')
df_devices = corregir_float(df_devices)
df_diagnosis = pd.read_csv('./csvs/_diagnosis.csv', delimiter = ',')
df_diagnosis = corregir_float(df_diagnosis)
df_ha_dates = pd.read_csv('./csvs/_hospital_admisions_F1.csv', delimiter=',')
df_ha_dates = corregir_float(df_ha_dates)
df_ha_info = pd.read_csv('./csvs/_hospital_admisions_F2.csv', delimiter=',')
df_ha_info = corregir_float(df_ha_info)
df_immunizations = pd.read_csv('./csvs/_immunizations.csv', delimiter=',')
df_immunizations = corregir_float(df_immunizations)
df_procedures = pd.read_csv('./csvs/_procedures.csv', delimiter=',')
df_procedures = corregir_float(df_procedures)
df_test_imaging_studies = pd.read_csv('./csvs/_test_imaging_studies.csv', delimiter=',')
df_test_imaging_studies = corregir_float(df_test_imaging_studies)
df_test_measurements = pd.read_csv('./csvs/_test_measurements.csv', delimiter=',')
df_test_measurements = corregir_float(df_test_measurements)
df_treatements_of_patients = pd.read_csv('./csvs/_treatements_of_patients_F1.csv', delimiter=',')
df_treatements_of_patients = corregir_float(df_treatements_of_patients)
df_patients = pd.read_csv('./csvs/_patients.csv', delimiter=',')
df_patients = corregir_float(df_patients)
df_providers = pd.read_csv('./csvs/_providers.csv', delimiter=',')
df_providers = corregir_float(df_providers)
df_organizations = pd.read_csv('./csvs/_organizations.csv', delimiter=',')
df_organizations = corregir_float(df_organizations)

# Subsets de organizations, que luego se usarán para filtrar también los datos del resto de tablas. Filtrado artificial de 10 organizaciones distintas para cada subset, con 1 en común
df_organizations_subset_1 = df_organizations[df_organizations['Id'].isin([
    '24cb4eab-6166-3530-bddc-a5a8a14a4fc1',
    '37c0de84-bcaf-3624-82bf-a89b2ac441b8',
    'ef58ea08-d883-3957-8300-150554edc8fb',
    'c44f361c-2efb-3050-8f97-0354a12e2920',
    'db0acede-4abe-3c01-8d03-5c68a190d8c7',
    'f1fbcbfb-fcfa-3bd2-b7f4-df20f1b3c3a4',
    '6f122869-a856-3d65-8db9-099bf4f5bbb8',
    '3fbe3da9-8e41-3118-a253-7e2d1b46480f',
    '23834663-ed53-3da9-b330-d6e1ecb8428e',
    '5d4b9df1-93ae-3bc9-b680-03249990e558'
])]
df_organizations_subset_2 = df_organizations[df_organizations['Id'].isin([
    '24cb4eab-6166-3530-bddc-a5a8a14a4fc1',
    '465de31f-3098-365c-af70-48a071e1f5aa',
    'a7500efb-720b-3e44-990a-0c3edc5a3990',
    'd311e70d-86e7-3c03-b115-53892bcf7ef1',
    'ac8356a5-78f8-3a63-8a1e-59e832fd54e7',
    'fd328395-ab1d-35c6-a2d0-d05a9a79cf11',
    'ecc51621-0af3-3b35-ac3e-8b1e34022e92',
    'ed146054-9dd5-3f0b-83df-d29d983039c3',
    '0b78995f-8b45-34d3-969d-afcc456bb1c7',
    '8ad64ecf-c817-3753-bee7-006a8e662e06'
])]

df_encounters_subset_1 = pd.merge(df_encounters, df_organizations_subset_1['Id'], how='inner', left_on='ORGANIZATION', right_on='Id').drop(columns = 'Id_y').rename(columns = {'Id_x': 'Id'})
df_encounters_subset_2 = pd.merge(df_encounters, df_organizations_subset_2['Id'], how='inner', left_on='ORGANIZATION', right_on='Id').drop(columns = 'Id_y').rename(columns = {'Id_x': 'Id'})


df_devices_subset_1 = pd.merge(df_devices, df_encounters_subset_1['Id'], how='inner', left_on='ENCOUNTER', right_on='Id').drop(columns = 'Id')
df_devices_subset_2 = pd.merge(df_devices, df_encounters_subset_2['Id'], how='inner', left_on='ENCOUNTER', right_on='Id').drop(columns = 'Id')

df_diagnosis_subset_1 = pd.merge(df_diagnosis, df_encounters_subset_1['Id'], how='inner', left_on='ENCOUNTER', right_on='Id').drop(columns = 'Id')
df_diagnosis_subset_2 = pd.merge(df_diagnosis, df_encounters_subset_2['Id'], how='inner', left_on='ENCOUNTER', right_on='Id').drop(columns = 'Id')

df_ha_dates_subset_1 = pd.merge(df_ha_dates, df_encounters_subset_1['Id'], how='inner', left_on='encounter', right_on='Id').drop(columns = 'Id')
df_ha_dates_subset_2 = pd.merge(df_ha_dates, df_encounters_subset_2['Id'], how='inner', left_on='encounter', right_on='Id').drop(columns = 'Id')

df_ha_info_subset_1 = pd.merge(df_ha_info, df_ha_dates_subset_1[['PatientID', 'AdmissionID']], how='inner', left_on=['PatientID', 'AdmissionID'], right_on=['PatientID', 'AdmissionID'])
df_ha_info_subset_2 = pd.merge(df_ha_info, df_ha_dates_subset_2[['PatientID', 'AdmissionID']], how='inner', left_on=['PatientID', 'AdmissionID'], right_on=['PatientID', 'AdmissionID'])

df_immunizations_subset_1 = pd.merge(df_immunizations, df_encounters_subset_1['Id'], how='inner', left_on='ENCOUNTER', right_on='Id').drop(columns = 'Id')
df_immunizations_subset_2 = pd.merge(df_immunizations, df_encounters_subset_2['Id'], how='inner', left_on='ENCOUNTER', right_on='Id').drop(columns = 'Id')

df_procedures_subset_1 = pd.merge(df_procedures, df_encounters_subset_1['Id'], how='inner', left_on='ENCOUNTER', right_on='Id').drop(columns = 'Id')
df_procedures_subset_2 = pd.merge(df_procedures, df_encounters_subset_2['Id'], how='inner', left_on='ENCOUNTER', right_on='Id').drop(columns = 'Id')

df_test_imaging_studies_subset_1 = pd.merge(df_test_imaging_studies, df_encounters_subset_1['Id'], how='inner', left_on='ENCOUNTER', right_on='Id').drop(columns = 'Id_y').rename(columns = {'Id_x': 'Id'})
df_test_imaging_studies_subset_2 = pd.merge(df_test_imaging_studies, df_encounters_subset_2['Id'], how='inner', left_on='ENCOUNTER', right_on='Id').drop(columns = 'Id_y').rename(columns = {'Id_x': 'Id'})

df_test_measurements_subset_1 = pd.merge(df_test_measurements, df_encounters_subset_1['Id'], how='inner', left_on='ENCOUNTER', right_on='Id').drop(columns = 'Id')
df_test_measurements_subset_2 = pd.merge(df_test_measurements, df_encounters_subset_2['Id'], how='inner', left_on='ENCOUNTER', right_on='Id').drop(columns = 'Id')

df_treatements_of_patients_subset_1 = pd.merge(df_treatements_of_patients, df_encounters_subset_1['Id'], how='inner', left_on='ENCOUNTER', right_on='Id').drop(columns = 'Id')
df_treatements_of_patients_subset_2 = pd.merge(df_treatements_of_patients, df_encounters_subset_2['Id'], how='inner', left_on='ENCOUNTER', right_on='Id').drop(columns = 'Id')


# Subsets de tablas que se relacionan con encounters 1:*
df_encounters_subset_1_providers = df_encounters_subset_1['PROVIDER'].dropna().unique()
df_encounters_subset_2_providers = df_encounters_subset_2['PROVIDER'].dropna().unique()
df_encounters_subset_1_patients = df_encounters_subset_1['PATIENT'].dropna().unique()
df_encounters_subset_2_patients = df_encounters_subset_2['PATIENT'].dropna().unique()

df_providers_subset_1 = df_providers[df_providers['Id'].isin(df_encounters_subset_1_providers)][['Id', 'ORGANIZATION', 'NAME', 'GENDER', 'SPECIALITY', 'ADDRESS', 'CITY', 'STATE', 'ZIP']]
df_providers_subset_2 = df_providers[df_providers['Id'].isin(df_encounters_subset_2_providers)][['Id', 'ORGANIZATION', 'LAT', 'LON', 'UTILIZATION']]


df_patients_subset_1 = df_patients[df_patients['Id'].isin(df_encounters_subset_1_patients)]
df_patients_subset_2 = df_patients[df_patients['Id'].isin(df_encounters_subset_2_patients)]


# Exportar todo a csvs

def guardar_csv(df, ruta):
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    df.to_csv(ruta, index=False)

guardar_csv(df_encounters_subset_1, 'csvs/subsets_3/encounters_subset_3.csv')
guardar_csv(df_encounters_subset_2, 'csvs/subsets_4/encounters_subset_4.csv')
guardar_csv(df_devices_subset_1, 'csvs/subsets_3/devices_subset_3.csv')
guardar_csv(df_devices_subset_2, 'csvs/subsets_4/devices_subset_4.csv')
guardar_csv(df_diagnosis_subset_1, 'csvs/subsets_3/diagnosis_subset_3.csv')
guardar_csv(df_diagnosis_subset_2, 'csvs/subsets_4/diagnosis_subset_4.csv')
guardar_csv(df_ha_dates_subset_1, 'csvs/subsets_3/hospital_admisions_F1_subset_3.csv')
guardar_csv(df_ha_dates_subset_2, 'csvs/subsets_4/hospital_admisions_F1_subset_4.csv')
guardar_csv(df_ha_info_subset_1, 'csvs/subsets_3/hospital_admisions_F2_subset_3.csv')
guardar_csv(df_ha_info_subset_2, 'csvs/subsets_4/hospital_admisions_F2_subset_4.csv')
guardar_csv(df_immunizations_subset_1, 'csvs/subsets_3/immunizations_subset_3.csv')
guardar_csv(df_immunizations_subset_2, 'csvs/subsets_4/immunizations_subset_4.csv')
guardar_csv(df_procedures_subset_1, 'csvs/subsets_3/procedures_subset_3.csv')
guardar_csv(df_procedures_subset_2, 'csvs/subsets_4/procedures_subset_4.csv')
guardar_csv(df_test_imaging_studies_subset_1, 'csvs/subsets_3/test_imaging_studies_subset_3.csv')
guardar_csv(df_test_imaging_studies_subset_2, 'csvs/subsets_4/test_imaging_studies_subset_4.csv')
guardar_csv(df_test_measurements_subset_1, 'csvs/subsets_3/test_measurements_subset_3.csv')
guardar_csv(df_test_measurements_subset_2, 'csvs/subsets_4/test_measurements_subset_4.csv')
guardar_csv(df_treatements_of_patients_subset_1, 'csvs/subsets_3/treatements_of_patients_subset_3.csv')
guardar_csv(df_treatements_of_patients_subset_2, 'csvs/subsets_4/treatements_of_patients_subset_4.csv')
guardar_csv(df_providers_subset_1, 'csvs/subsets_3/providers_subset_3.csv')
guardar_csv(df_providers_subset_2, 'csvs/subsets_4/providers_subset_4.csv')
guardar_csv(df_organizations_subset_1, 'csvs/subsets_3/organizations_subset_3.csv')
guardar_csv(df_organizations_subset_2, 'csvs/subsets_4/organizations_subset_4.csv')
guardar_csv(df_patients_subset_1, 'csvs/subsets_3/patients_subset_3.csv')
guardar_csv(df_patients_subset_2, 'csvs/subsets_4/patients_subset_4.csv')
