# Build da aplicação
FROM node:18-alpine AS builder

WORKDIR /app

# Copiar package.json
COPY package.json ./

# Instalar dependências usando npm
RUN npm install

# Copiar código fonte
COPY . .

# Verificar se o script build existe no package.json
RUN cat package.json | grep -A 5 -B 5 "scripts"

# Build da aplicação com verificação explícita
RUN npm run build && echo "Build completed successfully" && ls -la

# Verificar se a pasta dist foi criada
RUN if [ ! -d "dist" ]; then echo "ERROR: dist folder not found after build!"; ls -la; exit 1; fi

# Verificar conteúdo da pasta dist
RUN echo "Contents of dist folder:" && ls -la dist/

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

