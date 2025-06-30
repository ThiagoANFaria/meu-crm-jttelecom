# 1) Build da aplicação
FROM node:18-alpine AS builder
WORKDIR /app

# Instala só as deps
COPY package.json package-lock.json ./
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
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
