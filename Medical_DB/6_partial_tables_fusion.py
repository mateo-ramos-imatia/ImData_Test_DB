import pandas as pd

'''
Fusión de los datos que aparezcan divididos en más de 1 CSV.
A saber: patients y diagnosis, que ya vienen separados en la BBDD original, + encounters, que generamos nosotros un segundo csv en un script anterior
Diseases no será fusionada, ya que no la estamos usando para nada
'''

def corregir_float(df):
    for col in df.select_dtypes(include='float'):
        # Verificamos si todos los valores no nulos son enteros
        if df[col].dropna().apply(float.is_integer).all():
            df[col] = df[col].astype('Int64')
    return df

# Fusionando los encounters

df_encounters_1 = pd.read_csv('./csvs/_encounters_F1.csv', delimiter = ',')
df_encounters_2 = pd.read_csv('./csvs/_encounters_F2.csv', delimiter = ',')

df_encounters_1 = corregir_float(df_encounters_1)
df_encounters_2 = corregir_float(df_encounters_2)

df_encounters_1['START'] = pd.to_datetime(df_encounters_1['START'], utc=True)
df_encounters_1['STOP'] = pd.to_datetime(df_encounters_1['STOP'], utc=True)
df_encounters_2['START'] = pd.to_datetime(df_encounters_2['START'], utc=True)
df_encounters_2['STOP'] = pd.to_datetime(df_encounters_2['STOP'], utc=True)

df_encounters = pd.concat([df_encounters_1, df_encounters_2], ignore_index=True, sort=False)

df_encounters.to_csv('csvs/_encounters.csv', index=False)

# Fusionando los pacientes

df_patients_3 = pd.read_csv('./csvs/_Patients_3.csv', delimiter = '\t')
df_patients_4 = pd.read_csv('./csvs/_Patients_4.csv', delimiter = ',')

df_patients_3 = corregir_float(df_patients_3)
df_patients_4 = corregir_float(df_patients_4)

df_patients_3['PatientDateOfBirth'] = pd.to_datetime(df_patients_3['PatientDateOfBirth'], utc=True).dt.date
df_patients_4['BIRTHDATE'] = pd.to_datetime(df_patients_4['BIRTHDATE'], utc=True).dt.date
df_patients_4['DEATHDATE'] = pd.to_datetime(df_patients_4['DEATHDATE'], utc=True).dt.date

df_patients_3_renombrado = df_patients_3.rename(columns={
    'PatientID': 'Id',
    'PatientGender': 'GENDER',
    'PatientDateOfBirth': 'BIRTHDATE',
    'PatientRace': 'RACE',
    'PatientMaritalStatus': 'MARITAL',
    'PatientLanguage': 'LANGUAGE',
    'PatientPopulationPercentageBelowPoverty': 'PATIENTPOPULATIONPERCENTAGEBELOWPOVERTY'
})

df_patients = pd.concat([df_patients_4, df_patients_3_renombrado], ignore_index=True, sort=False)

df_patients.to_csv('csvs/_patients.csv', index=False)


# Fusionando los diagnosis

df_diagnosis_1 = pd.read_csv('./csvs/_diagnosis_1.csv', delimiter = ',')
df_diagnosis_2 = pd.read_csv('./csvs/_diagnosis_2.csv', delimiter = ',')

df_diagnosis_1 = corregir_float(df_diagnosis_1)
df_diagnosis_2 = corregir_float(df_diagnosis_2)

df_diagnosis_1['START'] = pd.to_datetime(df_diagnosis_1['START'], utc=True).dt.date
df_diagnosis_1['STOP'] = pd.to_datetime(df_diagnosis_1['STOP'], utc=True).dt.date
df_diagnosis_2['START'] = pd.to_datetime(df_diagnosis_2['START'], utc=True).dt.date
df_diagnosis_2['STOP'] = pd.to_datetime(df_diagnosis_2['STOP'], utc=True).dt.date

df_diagnosis= pd.concat([df_diagnosis_1, df_diagnosis_2], ignore_index=True, sort=False)

df_diagnosis.to_csv('csvs/_diagnosis.csv', index=False)