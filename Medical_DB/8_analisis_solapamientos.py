import pandas as pd

def corregir_float(df):
    for col in df.select_dtypes(include='float'):
        # Verificamos si todos los valores no nulos son enteros
        if df[col].dropna().apply(float.is_integer).all():
            df[col] = df[col].astype('Int64')
    return df

print ('---------------------------------\n',
       '---------- SUBSETS 1-2 ----------\n',
       '---------------------------------\n')
print ('---------- PACIENTES ----------')

df_patients_subset_1 = pd.read_csv('./csvs/subsets_1/patients_subset_1.csv', delimiter = ',')
df_patients_subset_1 = corregir_float(df_patients_subset_1)
df_patients_subset_2 = pd.read_csv('./csvs/subsets_2/patients_subset_2.csv', delimiter = ',')
df_patients_subset_2 = corregir_float(df_patients_subset_2)

df_patients_subset_2_ids = df_patients_subset_2['Id'].dropna().unique()
df_solapamiento_pacientes_1_2 = df_patients_subset_1[df_patients_subset_1['Id'].isin(df_patients_subset_2_ids)]['Id'].dropna().unique()
df_patients_subset_1_ids = df_patients_subset_1['Id'].dropna().unique()
df_solapamiento_pacientes_2_1 = df_patients_subset_2[df_patients_subset_2['Id'].isin(df_patients_subset_1_ids)]['Id'].dropna().unique()


print('------ Subset 1 ------\nVolumetría: ', len(df_patients_subset_1['Id'].dropna().unique()), '\n',
      'Solapamiento: ', len(df_solapamiento_pacientes_1_2), '\n',
      'Porcentaje de solapamiento: ', round(len(df_solapamiento_pacientes_1_2) * 100 / len(df_patients_subset_1['Id'].dropna().unique()), 2), '%')

print('------ Subset 2 ------\nVolumetría: ', len(df_patients_subset_2['Id'].dropna().unique()), '\n',
      'Solapamiento: ', len(df_solapamiento_pacientes_2_1), '\n',
      'Porcentaje de solapamiento: ', round(len(df_solapamiento_pacientes_2_1) * 100 / len(df_patients_subset_2['Id'].dropna().unique()), 2), '%')


print ('\n\n---------- ORGANIZACIONES ----------')

df_organizations_subset_1 = pd.read_csv('./csvs/subsets_1/organizations_subset_1.csv', delimiter = ',')
df_organizations_subset_1 = corregir_float(df_organizations_subset_1)
df_organizations_subset_2 = pd.read_csv('./csvs/subsets_2/organizations_subset_2.csv', delimiter = ',')
df_organizations_subset_2 = corregir_float(df_organizations_subset_2)

df_organizations_subset_2_ids = df_organizations_subset_2['Id'].dropna().unique()
df_solapamiento_pacientes_1_2 = df_organizations_subset_1[df_organizations_subset_1['Id'].isin(df_organizations_subset_2_ids)]['Id'].dropna().unique()
df_organizations_subset_1_ids = df_organizations_subset_1['Id'].dropna().unique()
df_solapamiento_pacientes_2_1 = df_organizations_subset_2[df_organizations_subset_2['Id'].isin(df_organizations_subset_1_ids)]['Id'].dropna().unique()


print('------ Subset 1 ------\nVolumetría: ', len(df_organizations_subset_1['Id'].dropna().unique()), '\n',
      'Solapamiento: ', len(df_solapamiento_pacientes_1_2), '\n',
      'Porcentaje de solapamiento: ', round(len(df_solapamiento_pacientes_1_2) * 100 / len(df_organizations_subset_1['Id'].dropna().unique()), 2), '%')

print('------ Subset 2 ------\nVolumetría: ', len(df_organizations_subset_2['Id'].dropna().unique()), '\n',
      'Solapamiento: ', len(df_solapamiento_pacientes_2_1), '\n',
      'Porcentaje de solapamiento: ', round(len(df_solapamiento_pacientes_2_1) * 100 / len(df_organizations_subset_2['Id'].dropna().unique()), 2), '%')


print ('\n\n---------- PROVEEDORES ----------')

df_providers_subset_1 = pd.read_csv('./csvs/subsets_1/providers_subset_1.csv', delimiter = ',')
df_providers_subset_1 = corregir_float(df_providers_subset_1)
df_providers_subset_2 = pd.read_csv('./csvs/subsets_2/providers_subset_2.csv', delimiter = ',')
df_providers_subset_2 = corregir_float(df_providers_subset_2)

df_providers_subset_2_ids = df_providers_subset_2['Id'].dropna().unique()
df_solapamiento_pacientes_1_2 = df_providers_subset_1[df_providers_subset_1['Id'].isin(df_providers_subset_2_ids)]['Id'].dropna().unique()
df_providers_subset_1_ids = df_providers_subset_1['Id'].dropna().unique()
df_solapamiento_pacientes_2_1 = df_providers_subset_2[df_providers_subset_2['Id'].isin(df_providers_subset_1_ids)]['Id'].dropna().unique()


print('------ Subset 1 ------\nVolumetría: ', len(df_providers_subset_1['Id'].dropna().unique()), '\n',
      'Solapamiento: ', len(df_solapamiento_pacientes_1_2), '\n',
      'Porcentaje de solapamiento: ', round(len(df_solapamiento_pacientes_1_2) * 100 / len(df_providers_subset_1['Id'].dropna().unique()), 2), '%')

print('------ Subset 2 ------\nVolumetría: ', len(df_providers_subset_2['Id'].dropna().unique()), '\n',
      'Solapamiento: ', len(df_solapamiento_pacientes_2_1), '\n',
      'Porcentaje de solapamiento: ', round(len(df_solapamiento_pacientes_2_1) * 100 / len(df_providers_subset_2['Id'].dropna().unique()), 2), '%')






print ('---------------------------------\n',
       '---------- SUBSETS 3-4 ----------\n',
       '---------------------------------\n')
print ('---------- PACIENTES ----------')

df_patients_subset_3 = pd.read_csv('./csvs/subsets_3/patients_subset_3.csv', delimiter = ',')
df_patients_subset_3 = corregir_float(df_patients_subset_3)
df_patients_subset_4 = pd.read_csv('./csvs/subsets_4/patients_subset_4.csv', delimiter = ',')
df_patients_subset_4 = corregir_float(df_patients_subset_4)

df_patients_subset_4_ids = df_patients_subset_4['Id'].dropna().unique()
df_solapamiento_pacientes_3_4 = df_patients_subset_3[df_patients_subset_3['Id'].isin(df_patients_subset_4_ids)]['Id'].dropna().unique()
df_patients_subset_3_ids = df_patients_subset_3['Id'].dropna().unique()
df_solapamiento_pacientes_4_3 = df_patients_subset_4[df_patients_subset_4['Id'].isin(df_patients_subset_3_ids)]['Id'].dropna().unique()


print('------ Subset 3 ------\nVolumetría: ', len(df_patients_subset_3['Id'].dropna().unique()), '\n',
      'Solapamiento: ', len(df_solapamiento_pacientes_3_4), '\n',
      'Porcentaje de solapamiento: ', round(len(df_solapamiento_pacientes_3_4) * 100 / len(df_patients_subset_3['Id'].dropna().unique()), 2), '%')

print('------ Subset 4 ------\nVolumetría: ', len(df_patients_subset_4['Id'].dropna().unique()), '\n',
      'Solapamiento: ', len(df_solapamiento_pacientes_4_3), '\n',
      'Porcentaje de solapamiento: ', round(len(df_solapamiento_pacientes_4_3) * 100 / len(df_patients_subset_4['Id'].dropna().unique()), 2), '%')


print ('\n\n---------- ENCOUNTERS ----------')

df_encounters_subset_3 = pd.read_csv('./csvs/subsets_3/encounters_subset_3.csv', delimiter = ',')
df_encounters_subset_3 = corregir_float(df_encounters_subset_3)
df_encounters_subset_4 = pd.read_csv('./csvs/subsets_4/encounters_subset_4.csv', delimiter = ',')
df_encounters_subset_4 = corregir_float(df_encounters_subset_4)

df_encounters_subset_4_ids = df_encounters_subset_4['Id'].dropna().unique()
df_solapamiento_pacientes_3_4 = df_encounters_subset_3[df_encounters_subset_3['Id'].isin(df_encounters_subset_4_ids)]['Id'].dropna().unique()
df_encounters_subset_3_ids = df_encounters_subset_3['Id'].dropna().unique()
df_solapamiento_pacientes_4_3 = df_encounters_subset_4[df_encounters_subset_4['Id'].isin(df_encounters_subset_3_ids)]['Id'].dropna().unique()


print('------ Subset 3 ------\nVolumetría: ', len(df_encounters_subset_3['Id'].dropna().unique()), '\n',
      'Solapamiento: ', len(df_solapamiento_pacientes_3_4), '\n',
      'Porcentaje de solapamiento: ', round(len(df_solapamiento_pacientes_3_4) * 100 / len(df_encounters_subset_3['Id'].dropna().unique()), 2), '%')

print('------ Subset 4 ------\nVolumetría: ', len(df_encounters_subset_4['Id'].dropna().unique()), '\n',
      'Solapamiento: ', len(df_solapamiento_pacientes_4_3), '\n',
      'Porcentaje de solapamiento: ', round(len(df_solapamiento_pacientes_4_3) * 100 / len(df_encounters_subset_4['Id'].dropna().unique()), 2), '%')


print ('\n\n---------- PROVEEDORES ----------')

df_providers_subset_3 = pd.read_csv('./csvs/subsets_3/providers_subset_3.csv', delimiter = ',')
df_providers_subset_3 = corregir_float(df_providers_subset_3)
df_providers_subset_4 = pd.read_csv('./csvs/subsets_4/providers_subset_4.csv', delimiter = ',')
df_providers_subset_4 = corregir_float(df_providers_subset_4)

df_providers_subset_4_ids = df_providers_subset_4['Id'].dropna().unique()
df_solapamiento_pacientes_3_4 = df_providers_subset_3[df_providers_subset_3['Id'].isin(df_providers_subset_4_ids)]['Id'].dropna().unique()
df_providers_subset_3_ids = df_providers_subset_3['Id'].dropna().unique()
df_solapamiento_pacientes_4_3 = df_providers_subset_4[df_providers_subset_4['Id'].isin(df_providers_subset_3_ids)]['Id'].dropna().unique()


print('------ Subset 3 ------\nVolumetría: ', len(df_providers_subset_3['Id'].dropna().unique()), '\n',
      'Solapamiento: ', len(df_solapamiento_pacientes_3_4), '\n',
      'Porcentaje de solapamiento: ', round(len(df_solapamiento_pacientes_3_4) * 100 / len(df_providers_subset_3['Id'].dropna().unique()), 2), '%')

print('------ Subset 4 ------\nVolumetría: ', len(df_providers_subset_4['Id'].dropna().unique()), '\n',
      'Solapamiento: ', len(df_solapamiento_pacientes_4_3), '\n',
      'Porcentaje de solapamiento: ', round(len(df_solapamiento_pacientes_4_3) * 100 / len(df_providers_subset_4['Id'].dropna().unique()), 2), '%')