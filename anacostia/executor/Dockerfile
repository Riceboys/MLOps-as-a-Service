# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# install curl
RUN apt-get update && apt-get install -y curl

# Install the Python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Python script to the working directory
COPY main.py .

# Set the command to run the Python script
#CMD ["nohup", "python", "-u", "main.py", "2>&1", "&"]
CMD ["python", "main.py"]

# display terminal outputs during image build (caching disabled):
# $ docker build --progress=plain --no-cache -t fairs-prod .

# display containers that have exited:
# $ docker ps -a