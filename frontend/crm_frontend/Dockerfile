# Build da aplicação
FROM node:20-slim AS builder

WORKDIR /app

# Instalar dependências do sistema necessárias para o build
RUN apt-get update && apt-get install -y \
    git \
    python3 \
    make \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Instalar pnpm globalmente
RUN npm install -g pnpm

# Copiar arquivos de dependências
COPY package.json pnpm-lock.yaml ./

# Limpar cache e instalar dependências
RUN pnpm store prune && pnpm install

# Copiar código fonte
COPY . .

# Build da aplicação com mais memória disponível
ENV NODE_OPTIONS="--max-old-space-size=4096"
RUN pnpm build

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

