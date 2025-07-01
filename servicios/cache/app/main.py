from fastapi import FastAPI, HTTPException
from cache import cache
import requests
import os
import json
import time
from statistics import mean

ELASTICSEARCH_URL = os.getenv("ELASTICSEARCH_URL", "http://elasticsearch:9200")
TTL = int(os.getenv("TTL_CACHE", 3600))

# Variables globales para métricas
hit_times = []
miss_times = []
total_hits = 0
total_misses = 0

app = FastAPI()

@app.get("/eventos/{evento_id}", status_code=200)
async def leer_evento_cache(evento_id: str):
    global total_hits, total_misses
    start = time.time()
    cached_event = cache.get(evento_id)
    if cached_event:
        elapsed = time.time() - start
        hit_times.append(elapsed)
        total_hits += 1
        return {"message": "CACHE", "data": json.loads(cached_event), "response_time": elapsed}
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
                cache.set(evento_id, json.dumps(evento), ex=TTL)
                elapsed = time.time() - start
                miss_times.append(elapsed)
                total_misses += 1
                return {"message": f"ELASTICSEARCH ({index})", "data": evento, "response_time": elapsed}
    elapsed = time.time() - start
    miss_times.append(elapsed)
    total_misses += 1
    raise HTTPException(status_code=404, detail="Evento no encontrado en Elasticsearch")

@app.get("/cache/metrics")
def cache_metrics():
    info = cache.info()
    hits = info.get("keyspace_hits", 0)
    misses = info.get("keyspace_misses", 0)
    used_memory = info.get("used_memory", 0)
    total = hits + misses
    hit_rate = hits / total if total > 0 else 0
    avg_hit_time = mean(hit_times) if hit_times else 0
    avg_miss_time = mean(miss_times) if miss_times else 0
    return {
        "hits": hits,
        "misses": misses,
        "hit_rate": hit_rate,
        "used_memory": used_memory,
        "avg_hit_time": avg_hit_time,
        "avg_miss_time": avg_miss_time
    }

@app.delete("/eventos/{evento_id}")
def invalidate_cache(evento_id: str):
    cache.delete(evento_id)
    return {"message": f"Cache invalidada para {evento_id}"}
