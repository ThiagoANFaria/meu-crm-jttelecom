FROM python:3.11-slim

# Instalar dependências do sistema necessárias para PostgreSQL
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar tudo
COPY . .

# Instalar dependências básicas
RUN pip install --upgrade pip
RUN pip install Flask flask-cors Flask-SQLAlchemy Flask-JWT-Extended PyJWT \
    blinker click Jinja2 MarkupSafe Werkzeug itsdangerous \
    psycopg2-binary SQLAlchemy typing_extensions greenlet

# Expor porta
EXPOSE 5000

# Comando para rodar - usar caminho correto
CMD ["python", "backend/crm_backend/src/main.py"]
