# Multi-stage build para otimizar o tamanho da imagem final
FROM node:18-alpine AS builder

# Definir diretório de trabalho
WORKDIR /app

# Copiar arquivos de dependências
COPY package.json package-lock.json ./

# Instalar dependências (incluindo devDependencies para o build)
RUN npm install

# Copiar código-fonte
COPY . .

# Fazer build do projeto
RUN npm run build

# Verificar se a pasta dist foi criada
RUN ls -la dist/

# Estágio de produção com nginx
FROM nginx:stable-alpine

# Copiar arquivos buildados do estágio anterior
COPY --from=builder /app/dist /usr/share/nginx/html

# Copiar configuração customizada do nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expor porta 80
EXPOSE 80

# Comando para iniciar o nginx
CMD ["nginx", "-g", "daemon off;"]

