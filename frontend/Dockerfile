FROM node:20-alpine3.17

WORKDIR /app

COPY package.json .

RUN npm install
RUN npm install vite --save-dev


COPY . .


EXPOSE 5173

CMD [ "npx", "vite", "dev","--host" ]