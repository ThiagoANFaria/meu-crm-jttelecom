FROM python:3.11-slim

# Instalar dependências do sistema necessárias para PostgreSQL
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar tudo da pasta atual (backend/crm_backend)
COPY . .

# DEBUG: Verificar o que temos agora
RUN echo "=== ESTRUTURA ===" && ls -la
RUN echo "=== ARQUIVOS PYTHON ===" && find . -name "*.py"

# Instalar dependências básicas
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

# Agora o main.py deve estar diretamente na raiz do contexto
CMD ["python", "main.py"]
