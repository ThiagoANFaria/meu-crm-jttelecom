# Use sua imagem base
FROM python:3.11-slim

# Instala dependências de SO
RUN apt-get update \
 && apt-get install -y gcc libpq-dev \
 && rm -rf /var/lib/apt/lists/*

# Define /app como diretório de trabalho
WORKDIR /app

# 1) Copia apenas o requirements.txt e instala (cache de deps)
COPY requirements.txt .
RUN pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# 2) Copia TODO o restante do seu backend para /app
COPY . .

# Expõe a porta que o Flask usará
EXPOSE 5000

# Inicia o Flask
CMD ["python", "main.py"]
