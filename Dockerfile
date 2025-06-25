FROM python:3.11-slim

# Instalar dependências do sistema necessárias para PostgreSQL
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar tudo
COPY . .

# DEBUG: Verificar o que realmente temos
RUN echo "=== Estrutura atual ===" 
RUN ls -la
RUN echo "=== Verificar subpastas ==="
RUN find . -name "*.py" -type f
RUN find . -name "requirements.txt" -type f

# Instalar dependências básicas (todas as que sua aplicação precisa)
RUN pip install --upgrade pip
RUN pip install \
    Flask==2.3.3 \
    flask-cors==4.0.0 \
    Flask-SQLAlchemy==3.0.5 \
    Flask-JWT-Extended==4.5.3 \
    PyJWT==2.8.0 \
    python-dotenv==1.0.0 \
    SQLAlchemy==2.0.23 \
    psycopg2-binary==2.9.7 \
    blinker==1.7.0 \
    click==8.1.7 \
    Jinja2==3.1.2 \
    MarkupSafe==2.1.3 \
    Werkzeug==2.3.7 \
    itsdangerous==2.1.2

# Comando para executar - vamos descobrir onde está o main.py
CMD ["python", "main.py"]
