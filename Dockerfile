FROM python:3.11-slim

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar tudo primeiro
COPY . .

# Instalar dependências
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Navegar para o diretório da aplicação
WORKDIR /app/backend/crm_backend

# Expor porta
EXPOSE 5000

# Comando para rodar
CMD ["python", "src/main.py"]
