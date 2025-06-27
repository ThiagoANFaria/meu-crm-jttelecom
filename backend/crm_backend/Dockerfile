# backend/crm_backend/Dockerfile
FROM python:3.11-slim

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
  && rm -rf /var/lib/apt/lists/*

# Define o diretório de trabalho
WORKDIR /app

# Copia só o requirements e instala antes (cache de deps)
COPY backend/crm_backend/requirements.txt .
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copia todo o resto do código para /app
COPY backend/crm_backend/ .

EXPOSE 5000

# Define PYTHONPATH (se precisar apontar para /app/src)
ENV PYTHONPATH=/app

# Inicia a aplicação (main.py está agora em /app/main.py)
CMD ["python", "main.py"]
