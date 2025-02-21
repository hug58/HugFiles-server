# Usar una imagen base de Node.js con Alpine
FROM node:20-alpine3.17

# Instalar curl en Alpine
RUN apk add --no-cache curl

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar el package.json y package-lock.json
COPY package.json .

# Instalar dependencias
RUN npm install
RUN npm install vite --save-dev

# Copiar el resto del código
COPY . .

# Exponer el puerto de desarrollo de Vite
EXPOSE 5173

# Comando para iniciar el servidor de desarrollo de Vite
CMD ["npx", "vite", "dev", "--host"]