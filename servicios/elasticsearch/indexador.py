import pandas as pd
from elasticsearch import Elasticsearch
import os

csv_path = "outputs/eventos_filtrados.csv"
es_host = os.getenv("ELASTIC_URL", "http://localhost:9200")

es = Elasticsearch(es_host)

df = pd.read_csv(csv_path)

for _, row in df.iterrows():
    doc = row.to_dict()
    es.index(index="eventos", document=doc)

print("Indexación completa.")
