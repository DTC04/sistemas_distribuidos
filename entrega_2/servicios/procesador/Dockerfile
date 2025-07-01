FROM python:3.9-slim

# Crear directorios necesarios
RUN mkdir -p /root/scripts /root/dataset /root/results

# Instalar pandas
RUN pip install pandas

# Copiar scripts
COPY analisis_python.py /root/
COPY run_pipeline.sh /root/

# Hacer ejecutable el script
RUN chmod +x /root/run_pipeline.sh

# Comando por defecto
CMD ["/root/run_pipeline.sh"]
