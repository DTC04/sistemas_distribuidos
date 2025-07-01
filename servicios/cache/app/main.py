from fastapi import FastAPI, HTTPException
from cache import cache
import requests
import os

ELASTICSEARCH_URL = os.getenv("ELASTICSEARCH_URL", "http://elasticsearch:9200")
TTL = int(os.getenv("TTL_CACHE", 3600))

app = FastAPI()

@app.get("/eventos/{evento_id}", status_code=200)
async def leer_evento_cache(evento_id: str):
    # Buscar en Redis primero
    cached_event = cache.get(evento_id)
    if cached_event:
        return {"message": "CACHE", "data": cached_event}

    # Si no está en cache, buscar en los índices de Elasticsearch
    indices = ["eventos_tiempo", "eventos_tipo", "eventos_comuna"]

    for index in indices:
        response = requests.get(
            f"{ELASTICSEARCH_URL}/{index}/_search",
            json={
                "query": {
                    "match": {
                        "_id": evento_id
                    }
                }
            }
        )

        if response.status_code == 200:
            data = response.json()
            hits = data.get("hits", {}).get("hits", [])
            if hits:
                evento = hits[0]["_source"]
                cache.set(evento_id, str(evento), ex=TTL)
                return {"message": f"ELASTICSEARCH ({index})", "data": evento}

    raise HTTPException(status_code=404, detail="Evento no encontrado en Elasticsearch")
