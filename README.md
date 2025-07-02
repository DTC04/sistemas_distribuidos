# Trabajo semestral 🗿


## 📋 Requisitos
- Docker
- Solicitar crendenciales 🥵

## 🚄 Para probar 
1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/sebaaaap/sistemas_distribuidos.git
   ```
2. **Importante estar en el directororio del compose.yml**:
    ```bash
    cd sistemas_distribuidos/entrega_2/servicios
    ```
3. **Y crear .env y colocar sus credenciales**
   ```python
   MONGO_USER=
   MONGO_PASSWORD= 
   MONGO_CLUSTER=
   MONGO_DB=       
   MONGO_COLLECTION=
   ```
4. **Levantar servicios**
   ```bash
   docker compose up --build
   ```

## 🛠️ Proceso de análisis automático con Apache Pig

El proceso de análisis de datos con Apache Pig ahora se realiza de forma automática al levantar los servicios. No es necesario ejecutar manualmente los pasos anteriores, ya que el contenedor `procesador` se encarga de procesar los datos y generar los resultados en la carpeta correspondiente.

Puedes revisar los resultados generados en la carpeta `servicios/resultados_pig`.


## 🔎 Acceso a Elasticsearch y Kibana

- **Elasticsearch**: [http://localhost:9200](http://localhost:9200)
- **Kibana** (visualización): [http://localhost:5601](http://localhost:5601)




























