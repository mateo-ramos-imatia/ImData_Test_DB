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

# Subsets de encounters, que luego se usarán para filtrar también los datos del resto de tablas
df_encounters_subset_1 = df_encounters[pd.to_datetime(df_encounters['START']).dt.year.isin([2019, 2017, 2015, 2013])]
df_encounters_subset_2 = df_encounters[pd.to_datetime(df_encounters['START']).dt.year.isin([2020, 2018, 2016, 2014])]

# Subsets de tablas que se relacionan con encounters *:1
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
df_encounters_subset_1_organizations = df_encounters_subset_1['ORGANIZATION'].dropna().unique()
df_encounters_subset_2_organizations = df_encounters_subset_2['ORGANIZATION'].dropna().unique()
df_encounters_subset_1_patients = df_encounters_subset_1['PATIENT'].dropna().unique()
df_encounters_subset_2_patients = df_encounters_subset_2['PATIENT'].dropna().unique()

df_providers_subset_1 = df_providers[df_providers['Id'].isin(df_encounters_subset_1_providers)][['Id', 'ORGANIZATION', 'NAME', 'GENDER', 'SPECIALITY', 'ADDRESS', 'CITY', 'STATE', 'ZIP']]
df_providers_subset_2 = df_providers[df_providers['Id'].isin(df_encounters_subset_2_providers)][['Id', 'ORGANIZATION', 'LAT', 'LON', 'UTILIZATION']]

df_organizations_subset_1 = df_organizations[df_organizations['Id'].isin(df_encounters_subset_1_organizations)][['Id', 'NAME', 'ADDRESS', 'CITY', 'STATE', 'ZIP']]
df_organizations_subset_2 = df_organizations[df_organizations['Id'].isin(df_encounters_subset_2_organizations)][['Id', 'LAT', 'LON', 'PHONE', 'REVENUE', 'UTILIZATION']]

df_patients_subset_1 = df_patients[df_patients['Id'].isin(df_encounters_subset_1_patients)]
df_patients_subset_2 = df_patients[df_patients['Id'].isin(df_encounters_subset_2_patients)]


# Exportar todo a csvs

def guardar_csv(df, ruta):
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    df.to_csv(ruta, index=False)

guardar_csv(df_encounters_subset_1, 'csvs/subsets_1/encounters_subset_1.csv')
guardar_csv(df_encounters_subset_2, 'csvs/subsets_2/encounters_subset_2.csv')
guardar_csv(df_devices_subset_1, 'csvs/subsets_1/devices_subset_1.csv')
guardar_csv(df_devices_subset_2, 'csvs/subsets_2/devices_subset_2.csv')
guardar_csv(df_diagnosis_subset_1, 'csvs/subsets_1/diagnosis_subset_1.csv')
guardar_csv(df_diagnosis_subset_2, 'csvs/subsets_2/diagnosis_subset_2.csv')
guardar_csv(df_ha_dates_subset_1, 'csvs/subsets_1/hospital_admisions_F1_subset_1.csv')
guardar_csv(df_ha_dates_subset_2, 'csvs/subsets_2/hospital_admisions_F1_subset_2.csv')
guardar_csv(df_ha_info_subset_1, 'csvs/subsets_1/hospital_admisions_F2_subset_1.csv')
guardar_csv(df_ha_info_subset_2, 'csvs/subsets_2/hospital_admisions_F2_subset_2.csv')
guardar_csv(df_immunizations_subset_1, 'csvs/subsets_1/immunizations_subset_1.csv')
guardar_csv(df_immunizations_subset_2, 'csvs/subsets_2/immunizations_subset_2.csv')
guardar_csv(df_procedures_subset_1, 'csvs/subsets_1/procedures_subset_1.csv')
guardar_csv(df_procedures_subset_2, 'csvs/subsets_2/procedures_subset_2.csv')
guardar_csv(df_test_imaging_studies_subset_1, 'csvs/subsets_1/test_imaging_studies_subset_1.csv')
guardar_csv(df_test_imaging_studies_subset_2, 'csvs/subsets_2/test_imaging_studies_subset_2.csv')
guardar_csv(df_test_measurements_subset_1, 'csvs/subsets_1/test_measurements_subset_1.csv')
guardar_csv(df_test_measurements_subset_2, 'csvs/subsets_2/test_measurements_subset_2.csv')
guardar_csv(df_treatements_of_patients_subset_1, 'csvs/subsets_1/treatements_of_patients_subset_1.csv')
guardar_csv(df_treatements_of_patients_subset_2, 'csvs/subsets_2/treatements_of_patients_subset_2.csv')
guardar_csv(df_providers_subset_1, 'csvs/subsets_1/providers_subset_1.csv')
guardar_csv(df_providers_subset_2, 'csvs/subsets_2/providers_subset_2.csv')
guardar_csv(df_organizations_subset_1, 'csvs/subsets_1/organizations_subset_1.csv')
guardar_csv(df_organizations_subset_2, 'csvs/subsets_2/organizations_subset_2.csv')
guardar_csv(df_patients_subset_1, 'csvs/subsets_1/patients_subset_1.csv')
guardar_csv(df_patients_subset_2, 'csvs/subsets_2/patients_subset_2.csv')
