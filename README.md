# MLOps-as-a-Service

## Tasks Completed
- [X] Can automatically pull docker images from Docker Hub
- [X] Can automatically deploy pulled docker images as running containers
- [X] Executor can trigger functions (designated as code for preparing data and training) on the host machine via Flask API

## TODO
- [ ] Create CLI for Anacostia Executor (CLI allows host to trigger training pipeline manually)
- [ ] Enable Anacostia Executor to trigger training based on a schedule (via cron expression)
- [ ] Enable command line arguments for MLflow to be sent from host
- [ ] Add support for a model deployment service like Seldon Core or Triton
- [ ] Add support for logging to Weights & Biases and MLflow in Anacostia Client API (common API)
- [ ] Create python package for Anacostia Client API and push python package up to PyPI
- [ ] Create simple demo that shows:
    1. User pip installing Anacostia Client API
    2. User setting up and configuring pipeline (show configurations for Anacostia Executor and user specifying what components in the pipeline)
    3. User adding decorators to code to declare code for loading data, preparing data, training the model, evaluating model, deploying model
    4. Show user manually triggering pipeline for automatic retraining
