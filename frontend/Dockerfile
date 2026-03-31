# 1. Build React
FROM node:20-alpine AS build

WORKDIR /app

# Copiamos solo lo necesario para instalar dependencias
COPY package.json package-lock.json ./
RUN npm ci --legacy-peer-deps

# Copiamos el resto del código
COPY . .

# Variables de entorno para React
ARG REACT_APP_API_URL
ENV REACT_APP_API_URL=$REACT_APP_API_URL

# Observabilidad opcional
RUN echo "=== LISTANDO /app/src ===" && ls -R /app/src || true
RUN echo "=== LISTANDO /app/src/components ===" && ls -R /app/src/components || true

# Compilamos React
RUN npm run build

# 2. Servir con nginx
FROM nginx:alpine

# Copiamos el resultado del build al html de nginx
COPY --from=build /app/dist /usr/share/nginx/html

# Reemplazamos config nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf