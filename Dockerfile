# Use a base image with Python 3.10 (e.g., python:3.10)
FROM python:3.10

# Set environment variables to prevent interactive prompts during installation
ENV DEBIAN_FRONTEND=noninteractive

# Set environment variables
ENV APP_USER=bg
ENV APP_HOME=/app

# Create a non-root user and group
RUN useradd -m -s /bin/bash $APP_USER

# Update package list and install Tesseract OCR
RUN apt-get update && \
    apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-eng \
    libgl1-mesa-glx

# Install Google Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update && apt-get install -y google-chrome-stable \
    && apt-get clean

# Optionally, install any Python dependencies using pip
# COPY requirements.txt /app/requirements.txt

# Copy your Python application code to the container (assuming it's in the same directory as the Dockerfile)
COPY . /app

# Set the working directory inside the container
WORKDIR /app

# WORKDIR /app
RUN pip install -r requirements.txt

# Change ownership of the application files to the non-root user
RUN chown -R $APP_USER:$APP_USER $APP_HOME
RUN chmod -R 775 $APP_HOME

# Switch to the non-root user
USER $APP_USER

# Specify the command to run your Python application
CMD ["python", "app.py"]