FROM python:3.11-slim

# Instalar dependências do sistema necessárias para PostgreSQL
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar tudo
COPY . .

# DEBUG: Verificar estrutura real
RUN echo "=== Estrutura atual ===" 
RUN ls -la
RUN echo "=== Verificar se main.py existe ==="
RUN test -f main.py && echo "main.py EXISTE" || echo "main.py NÃO EXISTE"

# Instalar dependências básicas
RUN pip install --upgrade pip
RUN pip install Flask flask-cors Flask-SQLAlchemy Flask-JWT-Extended PyJWT \
    blinker click Jinja2 MarkupSafe Werkzeug itsdangerous \
    python-dotenv SQLAlchemy

# Instalar dependências específicas do projeto
RUN pip install -r requirements.txt

# Comando para executar o main.py (que está na raiz agora)
CMD ["python", "main.py"]
