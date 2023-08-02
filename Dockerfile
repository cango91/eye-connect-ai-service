# Start from the python:3.7-slim base image
FROM python:3.11-slim

# Install nginx
RUN apt-get update && apt-get install -y nginx

# Set the working directory in the Docker image to /app
WORKDIR /app

# Copy the requirements.txt file into the /app directory in the Docker image
COPY requirements.txt /app

# Install the Python dependencies without caching
RUN pip install --no-cache-dir -r requirements.txt

# Copy the model file, main.py, and the NGINX configuration file into the Docker image
COPY model.h5 /app
COPY main.py /app
COPY nginx.conf /etc/nginx/sites-available/

# Create a symbolic link to enable the NGINX configuration
RUN ln -s /etc/nginx/sites-available/nginx.conf /etc/nginx/sites-enabled/

# Remove the default NGINX configuration
RUN rm /etc/nginx/sites-enabled/default

# Expose the port that the Flask app is running on
EXPOSE 5001

# Start NGINX and the Flask app when the Docker container is started
CMD service nginx start && python main.py
