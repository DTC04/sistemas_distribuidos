import requests
import time
import random

# Configura la URL de tu microservicio de caché
CACHE_URL = "http://localhost:8001/eventos/{}"  # Cambia el puerto si es necesario

# Lista de IDs de eventos para consultar (puedes poner IDs reales de tu base)
eventos_ids = [
    "id1", "id2", "id3", "id4", "id5"
    # Agrega más IDs reales aquí
]

N = 100  # Número de consultas totales
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

# Estadísticas
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