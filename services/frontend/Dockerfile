FROM node:16.14.2

WORKDIR /app
COPY ./services/frontend/package*.json ./

RUN npm install --silent

COPY ./services/frontend .

EXPOSE 3000

CMD ["npm", "start"]
