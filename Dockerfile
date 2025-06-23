FROM python:3.9-slim

WORKDIR /app

# Copiar requirements
COPY backend/crm_backend/requirements.txt .

# Instalar dependências
RUN pip install -r requirements.txt

# Copiar código
COPY backend/crm_backend/ .

# Expor porta
EXPOSE 5000

# Comando para rodar
CMD ["python", "src/main.py"]
