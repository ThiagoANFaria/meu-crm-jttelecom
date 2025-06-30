# 1) Build da aplicação
FROM node:18-alpine AS builder

WORKDIR /app

# Instalar só as deps
COPY package.json pnpm-lock.yaml ./
RUN npm cache clean --force && npm ci

# Copia o código e gera o build
COPY . .

ARG VITE_API_URL
ARG VITE_APP_URL
ARG VITE_APP_NAME
ARG VITE_APP_VERSION
ARG VITE_ENVIRONMENT

RUN npm run build

# 2) Servir com Nginx
FROM nginx:stable-alpine

COPY --from=builder /app/dist /usr/share/nginx/html

# Copiar configuração customizada do nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expor porta 80
EXPOSE 80

# Comando para iniciar nginx
CMD ["nginx", "-g", "daemon off;"]

