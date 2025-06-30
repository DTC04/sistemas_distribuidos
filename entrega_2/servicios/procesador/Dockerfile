FROM fluddeni/hadoop-pig:latest

# Crear carpetas necesarias dentro del contenedor
RUN mkdir -p /root/scripts /root/dataset /root/results

# Copiar script de Pig y script de ejecución al contenedor
COPY analisis_general.pig /root/scripts/
COPY run_pipeline.sh /root/

# Dar permisos de ejecución al script
RUN chmod +x /root/run_pipeline.sh

# Comando por defecto al iniciar el contenedor
CMD ["/bin/bash", "/root/run_pipeline.sh"]
