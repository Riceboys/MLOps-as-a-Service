FROM ghcr.io/mlflow/mlflow:latest

WORKDIR /app

# install git
RUN apt-get update && apt-get install -y git

COPY requirements.txt requirements.txt

RUN mkdir /mlruns
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY main.py main.py

ENV MLFLOW_HOST="0.0.0.0"
ENV MLFLOW_PORT="5000"
ENV ANACOSTIA_PORT="8000"

# these environment variables might not be able to be set in the dockerfile
ENV MLFLOW_BACKEND_STORE_URI="file:///mlruns"
ENV MLFLOW_TRACKING_URI="file:///mlruns"
ENV MLFLOW_DEFAULT_ARTIFACT_ROOT="/artifacts"
