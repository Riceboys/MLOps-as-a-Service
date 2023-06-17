FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Python script to the working directory
COPY main.py .

# Set the command to run the Python script
CMD ["python", "main.py"]