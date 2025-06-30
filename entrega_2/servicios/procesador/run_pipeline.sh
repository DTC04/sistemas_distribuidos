#!/bin/bash

echo "Esperando a que HDFS esté disponible..."
sleep 10  

hdfs dfs -test -d /user/hadoop/ || hdfs dfs -mkdir -p /user/hadoop/

echo "Subiendo archivo CSV filtrado a HDFS..."
hdfs dfs -put -f /root/dataset/eventos_filtrados.csv /user/hadoop/

echo "Ejecutando análisis con Apache Pig..."
pig -x mapreduce -f /root/scripts/analisis_general.pig

mkdir -p /root/results/comuna /root/results/tipo /root/results/tiempo

echo "Descargando resultados desde HDFS..."
hdfs dfs -copyToLocal /user/hadoop/results/comuna/part-r-00000 /root/results/comuna/
hdfs dfs -copyToLocal /user/hadoop/results/tipo/part-r-00000 /root/results/tipo/
hdfs dfs -copyToLocal /user/hadoop/results/tiempo/part-r-00000 /root/results/tiempo/

(echo "comuna,total" && cat /root/results/comuna/part-r-00000) > /root/results/comuna/comuna.csv
(echo "tipo,total" && cat /root/results/tipo/part-r-00000) > /root/results/tipo/tipo.csv
(echo "fecha,total" && cat /root/results/tiempo/part-r-00000) > /root/results/tiempo/tiempo.csv

echo "Proceso completado correctamente."
