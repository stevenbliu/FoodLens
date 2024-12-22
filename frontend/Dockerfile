FROM node:16

WORKDIR /app
RUN apt-get update && apt-get install -y jq

COPY package.json .
RUN npm install
# RUN npm run clean

COPY . .
RUN chmod +x ./ngrok_url_fetcher.sh

CMD ./ngrok_url_fetcher.sh&& npm start
