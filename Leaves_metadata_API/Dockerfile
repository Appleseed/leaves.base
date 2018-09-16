FROM node:7
WORKDIR /app
COPY package.json /app
RUN npm install
RUN npm install open
RUN npm install webshot
RUN npm i --S redis
COPY . /app
CMD node index.js
EXPOSE 8081

