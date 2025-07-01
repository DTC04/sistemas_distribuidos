FROM python:3.9-slim

RUN mkdir -p /root/scripts /root/dataset /root/results

RUN pip install pandas

COPY analisis_python.py /root/
COPY run_pipeline.sh /root/

RUN chmod +x /root/run_pipeline.sh

CMD ["/root/run_pipeline.sh"]
