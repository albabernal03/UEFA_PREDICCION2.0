import pandas as pd

# Cargar los datos de las fases desde el archivo CSV existente
all_data_df = pd.read_csv('champions_results.csv')

# Cargar los datos de las finales desde el archivo CSV generado
final_data_df = pd.read_csv('final.csv')

# Concatenar ambos DataFrames
combined_data_df = pd.concat([all_data_df, final_data_df], ignore_index=True)

# Guardar el DataFrame combinado en un nuevo archivo CSV
combined_data_df.to_csv('combined_data.csv', index=False)
