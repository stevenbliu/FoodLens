#!/bin/bash
# Wait for ngrok to start
while [ -z "$(curl -s http://ngrok:4040/api/tunnels | jq -r '.tunnels[0].public_url')" ]; do
    echo "Waiting for ngrok to be ready..."
    sleep 1
done



# Get Ngrok public URL from the API
NGROK_PUBLIC_URL=$(curl -s http://ngrok:4040/api/tunnels | jq -r '.tunnels[0].public_url')
NGROK_PUBLIC_URL=$(echo "$NGROK_PUBLIC_URL" | sed 's|https://||')

# Overwrite the .env file with the new public URL
echo "REACT_APP_NGROK_PUBLIC_URL=$NGROK_PUBLIC_URL" > .env

echo "Ngrok public URL is $NGROK_PUBLIC_URL"

# Log the contents of the .env file
echo "The contents of the .env file are:"
cat .env

# Start the application (backend or frontend)
exec "$@"
