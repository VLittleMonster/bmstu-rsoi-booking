FROM node:16.14.2

WORKDIR /app
COPY ./frontend/package*.json ./

RUN npm install --silent

COPY ./frontend .

EXPOSE 3000

CMD ["npm", "start"]
