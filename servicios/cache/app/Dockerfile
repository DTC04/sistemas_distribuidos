FROM python:3.11-slim
WORKDIR /app
COPY test_cache_load.py .
RUN pip install requests
CMD ["python", "test_cache_load.py"]