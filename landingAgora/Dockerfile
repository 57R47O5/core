# 1. Build stage
FROM node:20-alpine AS build

WORKDIR /app

# Copiamos los archivos de dependencias de npm
COPY package.json package-lock.json ./
RUN npm ci --legacy-peer-deps

# Copiamos el resto del proyecto
COPY . .

# Build con React / Vite
ARG REACT_APP_API_URL
ENV REACT_APP_API_URL=$REACT_APP_API_URL
RUN npm run build

# 2. Serve stage
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]