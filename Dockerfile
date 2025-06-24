FROM python:3.11-slim

# Instalar dependências do sistema necessárias para PostgreSQL
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar tudo
COPY . .

# DEBUG: Verificar estrutura de arquivos
RUN echo "=== Estrutura da raiz ==="
RUN ls -la
RUN echo "=== Estrutura do backend ==="
RUN ls -la backend/
RUN echo "=== Estrutura do crm_backend ==="
RUN ls -la backend/crm_backend/
RUN echo "=== Estrutura do src ==="
RUN ls -la backend/crm_backend/src/
RUN echo "=== Verificar se main.py existe ==="
RUN test -f backend/crm_backend/src/main.py && echo "main.py EXISTE" || echo "main.py NÃO EXISTE"

# Instalar dependências básicas
RUN pip install --upgrade pip
RUN pip install Flask flask-cors Flask-SQLAlchemy Flask-JWT-Extended PyJWT \
    blinker click Jinja2 MarkupSafe Werkzeug itsdangerous \
    psycopg2-binary SQLAlchemy typing_extensions greenlet

# Expor porta
EXPOSE 5000

# Comando para rodar - usar caminho correto
CMD ["python", "backend/crm_backend/src/main.py"]
