# Use Python 3.9 as the base image
FROM python:3.11

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Install jq for fetching ngrok public URL (add this before copying the app code for better caching)
RUN apt-get update && apt-get install -y jq

# Copy the rest of the application code to the container
COPY . .

# Make the ngrok URL fetcher script executable
RUN chmod +x ./ngrok_url_fetcher.sh

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

# Run the ngrok URL fetcher script and start the Django development server
CMD ./ngrok_url_fetcher.sh && python manage.py runserver 0.0.0.0:8000 
#--noreload
