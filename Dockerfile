FROM python:3.11-slim

WORKDIR /app

# Copiar tudo
COPY . .

# Verificar se o arquivo existe (debug)
RUN ls -la
RUN cat requirements.txt

# Instalar dependências básicas
RUN pip install --upgrade pip
RUN pip install Flask flask-cors Flask-SQLAlchemy

# Navegar para o diretório da aplicação
WORKDIR /app/backend/crm_backend

# Expor porta
EXPOSE 5000

# Comando para rodar
CMD ["python", "src/main.py"]
