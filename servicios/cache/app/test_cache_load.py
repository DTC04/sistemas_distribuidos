import requests
import time
import random

CACHE_URL = "http://cache:8001/eventos/{}"  
eventos_ids = [
    "94b3c933-e169-4cb1-a5e8-13cc61159962",
    "ae5362a9-0b4e-42fe-a1e5-aa7dc2b8efd3",
    "7f24151d-7a9e-44fd-a451-2343f70fd144",
    "123e4567-e89b-12d3-a456-426614174000",
    "aa3d63d2-2ab9-4a48-aa35-78f6d0f72cd8",
]

# Esperar a que el servicio de caché esté disponible
for i in range(100):
    try:
        resp = requests.get("http://cache:8001/openapi.json")
        if resp.status_code == 200:
            print("Servicio de caché disponible.")
            break
    except Exception:
        print(f"Esperando a que el servicio de caché esté disponible... ({i+1}/100)")
        time.sleep(2)
else:
    print("No se pudo conectar al servicio de caché. Abortando test.")
    exit(1)

N = 100  
resultados = []

for i in range(N):
    evento_id = random.choice(eventos_ids)
    start = time.time()
    resp = requests.get(CACHE_URL.format(evento_id))
    elapsed = time.time() - start
    if resp.status_code == 200:
        origen = resp.json().get("message")
        resultados.append((origen, elapsed))
        print(f"[{i+1}] {evento_id} - {origen} - {elapsed:.4f} seg")
    else:
        print(f"[{i+1}] {evento_id} - ERROR")

hits = [r for r in resultados if r[0] == "CACHE"]
misses = [r for r in resultados if r[0] != "CACHE"]
print("\n--- Estadísticas ---")
print(f"Total consultas: {len(resultados)}")
print(f"Cache hits: {len(hits)}")
print(f"Cache misses: {len(misses)}")
if hits:
    print(f"Tiempo promedio (cache): {sum(r[1] for r in hits)/len(hits):.4f} seg")
if misses:
    print(f"Tiempo promedio (no cache): {sum(r[1] for r in misses)/len(misses):.4f} seg")