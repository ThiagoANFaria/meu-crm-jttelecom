# Build da aplicação
FROM node:18-alpine AS builder

WORKDIR /app

# Copiar package.json
COPY package.json ./

# Instalar dependências usando npm
RUN npm install

# Copiar código fonte
COPY . .

# Build da aplicação com logs detalhados
RUN npm run build 2>&1 | tee build.log || (echo "=== BUILD FAILED - SHOWING LOGS ===" && cat build.log && exit 1)

# Servir com Nginx
FROM nginx:stable-alpine

# Copiar arquivos buildados
COPY --from=builder /app/dist /usr/share/nginx/html

# Copiar configuração customizada do nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expor porta 80
EXPOSE 80

# Comando para iniciar nginx
CMD ["nginx", "-g", "daemon off;"]

