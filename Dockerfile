FROM python:3.9-slim

WORKDIR /app

COPY backend/crm_backend/requirements.txt .

RUN pip install -r requirements.txt

COPY backend/crm_backend/ .

EXPOSE 5000

CMD ["python", "src/main.py"]
