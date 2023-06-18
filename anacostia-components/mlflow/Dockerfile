FROM ghcr.io/mlflow/mlflow:latest

WORKDIR /app

COPY requirements.txt .

ENV BACKEND_URI file:///app/storage
ENV ARTIFACT_ROOT /app/storage

CMD mlflow server --backend-store-uri ${BACKEND_URI} --default-artifact-root ${ARTIFACT_ROOT} --host 0.0.0.0 --port 5000
