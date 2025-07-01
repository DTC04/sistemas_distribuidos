#!/usr/bin/env python3
import pandas as pd
import os
from collections import Counter

# Cargar datos
print("Cargando datos...")
df = pd.read_csv('/root/dataset/eventos_filtrados.csv')

print(f"Datos cargados: {len(df)} registros")

# Análisis por comuna
print("Analizando por comuna...")
comunas = []
for comuna_str in df['comuna']:
    if pd.notna(comuna_str):
        # Separar comunas múltiples
        comunas_individuales = [c.strip() for c in comuna_str.split(';')]
        comunas.extend(comunas_individuales)

conteo_comunas = Counter(comunas)
comunas_df = pd.DataFrame(list(conteo_comunas.items()), columns=['comuna', 'total'])

# Análisis por tipo
print("Analizando por tipo...")
conteo_tipos = df['tipo'].value_counts().reset_index()
conteo_tipos.columns = ['tipo', 'total']

# Análisis por fecha
print("Analizando por fecha...")
df['fecha'] = df['timestamp'].str[:10]  # Extraer solo la fecha
conteo_fechas = df['fecha'].value_counts().reset_index()
conteo_fechas.columns = ['fecha', 'total']

# Guardar resultados
print("Guardando resultados...")
os.makedirs('/root/results/comuna', exist_ok=True)
os.makedirs('/root/results/tipo', exist_ok=True)
os.makedirs('/root/results/tiempo', exist_ok=True)

comunas_df.to_csv('/root/results/comuna/comuna.csv', index=False)
conteo_tipos.to_csv('/root/results/tipo/tipo.csv', index=False)
conteo_fechas.to_csv('/root/results/tiempo/tiempo.csv', index=False)

print("Análisis completado exitosamente!")
print(f"Comunas analizadas: {len(comunas_df)}")
print(f"Tipos analizados: {len(conteo_tipos)}")
print(f"Fechas analizadas: {len(conteo_fechas)}") 