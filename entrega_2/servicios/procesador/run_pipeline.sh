#!/bin/bash

echo "Creando directorios de resultados..."
mkdir -p /root/results/comuna /root/results/tipo /root/results/tiempo

echo "Ejecutando análisis con Python..."
python /root/analisis_python.py

echo "Proceso completado correctamente."
