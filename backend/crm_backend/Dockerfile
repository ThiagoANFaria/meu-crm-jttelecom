FROM python:3.11-slim

# Definir diretório de trabalho
WORKDIR /app

# Copiar arquivo de requisitos
COPY requirements.txt .

# Instalar dependências
RUN apt-get update && apt-get install -y gcc libpq-dev && \
    pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY . .

# Expor porta
EXPOSE 5000

# Comando para executar a aplicação
CMD ["python", "src/main.py"]

