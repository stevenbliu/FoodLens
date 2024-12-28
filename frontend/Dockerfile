FROM node:16

WORKDIR /app
COPY frontend/package.json frontend/package-lock.json ./
# COPY . ./
COPY . .


RUN apt-get update && apt-get install -y jq

# COPY package.json .
RUN npm install
# RUN npm run clean

COPY frontend ./
COPY frontend/ngrok_url_fetcher.sh /app/ngrok_url_fetcher.sh

RUN chmod +x /app/ngrok_url_fetcher.sh

CMD /app/ngrok_url_fetcher.sh && npm start
