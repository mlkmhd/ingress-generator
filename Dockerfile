FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY create_ingress.py .

CMD ["kopf", "run", "--standalone", "create_ingress.py"]