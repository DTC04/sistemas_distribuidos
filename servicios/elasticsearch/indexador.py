import pandas as pd
from elasticsearch import Elasticsearch
import os
from datetime import datetime
import numpy as np
import time

es_host = os.getenv("ELASTIC_URL", "http://localhost:9200")
es = Elasticsearch(es_host)

max_reintentos = 20
for intento in range(1, max_reintentos + 1):
    try:
        if es.ping():
            print(f"Conexión exitosa a Elasticsearch en el intento {intento}.")
            break
        else:
            raise Exception("Elasticsearch no responde al ping.")
    except Exception as e:
        print(f"Intento {intento}/{max_reintentos}: Elasticsearch no está disponible aún. Esperando 3 segundos...")
        time.sleep(3)
else:
    print("No se pudo conectar a Elasticsearch después de varios intentos. Abortando indexación.")
    exit(1)

eventos_path = "outputs/eventos_filtrados.csv"
if os.path.exists(eventos_path):
    df = pd.read_csv(eventos_path)
    df = df.replace({np.nan: ""})  
    for _, row in df.iterrows():
        doc = row.to_dict()
        if 'timestamp' in doc:
            try:
                dt = pd.to_datetime(doc['timestamp'])
                doc['timestamp'] = dt.isoformat()
            except Exception:
                pass
        es.index(index="eventos", document=doc)
    print("Indexación de eventos_filtrados.csv completa.")
else:
    print(f"No se encontró {eventos_path}")

comuna_path = "../resultados_pig/comuna/comuna.csv"
if os.path.exists(comuna_path):
    df_comuna = pd.read_csv(comuna_path)
    df_comuna = df_comuna.replace({np.nan: ""})
    for _, row in df_comuna.iterrows():
        doc = row.to_dict()
        es.index(index="eventos_comuna", document=doc)
    print("Indexación de comuna.csv completa.")
else:
    print(f"No se encontró {comuna_path}")

tipo_path = "../resultados_pig/tipo/tipo.csv"
if os.path.exists(tipo_path):
    df_tipo = pd.read_csv(tipo_path)
    df_tipo = df_tipo.replace({np.nan: ""})  
    for _, row in df_tipo.iterrows():
        doc = row.to_dict()
        es.index(index="eventos_tipo", document=doc)
    print("Indexación de tipo.csv completa.")
else:
    print(f"No se encontró {tipo_path}")

tiempo_path = "../resultados_pig/tiempo/tiempo.csv"
if os.path.exists(tiempo_path):
    df_tiempo = pd.read_csv(tiempo_path)
    df_tiempo = df_tiempo.replace({np.nan: ""})  
    for _, row in df_tiempo.iterrows():
        doc = row.to_dict()
        if 'fecha' in doc:
            try:
                dt = pd.to_datetime(doc['fecha'])
                doc['fecha'] = dt.date().isoformat()
            except Exception:
                pass
        es.index(index="eventos_tiempo", document=doc)
    print("Indexación de tiempo.csv completa.")
else:
    print(f"No se encontró {tiempo_path}")

print("Indexación completa de todos los archivos.")
