FROM python:3.11-slim

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar tudo
COPY . .

# Definir o diretório correto
WORKDIR /app/backend/crm_backend

# Instalar dependências Python (usar o requirements.txt se existir)
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 5000

ENV PYTHONPATH=/app

CMD ["python", "main.py"]
