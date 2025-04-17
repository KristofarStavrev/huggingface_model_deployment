# huggingface_model_deployment

## TODO:
- [X] Upload model to HuggingFace modelhub
- [X] Productionize and modularize notebook code
- [X] Makefile
- [X] Dockerize
    - [X] Integrate poetry
    - [X] Separate the fastAPI backend and gradio frontend services in different containers
    - [X] Handle them with Docker compose
- [X] CI/CD
    - [X] Use a self-hosted CI/CD runner
    - [X] Use a self-hosted docker image repository
    - [X] Self-host the deployment environment
    - [X] Clean-up old images/containers on the prod server
    - [X] Enable image caching in the self-hosted runner
    - [X] Create an automated release when a new tag is created
    - [ ] FOR FUTURE IMPROVEMENTS: Tag docker images with release/commit tag
- [X] Code styling, linting, security and tests
    - [X] Pytest for unit/mock/integration tests
    - [X] Code coverage
    - [X] Bandit and pip-audit for catching security flaws
    - [X] Mypy for typechecking
    - [X] ruff for linting
    - [X] Integrate tests in the CI/CD (Optionally use Nox to orchestrate)
    - [ ] FOR FUTURE IMPROVEMENTS: More strict code styling and introduce pre-commit hooks
    - [ ] FOR FUTURE IMPROVEMENTS: Stub files that mypy can use for the custom modules (model_utils.py)
- [ ] Logs and messages
    - [ ] Logging in all src codes
    - [ ] Loki + Promtail
    - [ ] Prometheus
    - [ ] Grafana
    - [ ] FOR FUTURE IMPROVEMENTS: Kafka
- [ ] Kubernetes/Kserve/Helmchart + GPU
- [ ] Code refactoring and finishing touches
    - [ ] Training/Validation/Testing scripts and modularity
    - [ ] Documentation (MkDocs / Sphinx) + Docstrings
    - [ ] Documentation for the GitHub Read.me - how to start the app, etc.
- [IN PROGRESS] Create an diagram for the entire architecture (CI/CD, model retraining, etc.)

- [ ] FOR FUTURE IMPROVEMENTS: Deploy in AWS - EC2 or ECS
- [ ] FOR FUTURE IMPROVEMENTS: Terraform/Ansible for infrastructure
- [ ] FOR FUTURE IMPROVEMENTS: Model tracking, drift, automated retraining
- [ ] FOR FUTURE IMPROVEMENTS: Airflow/Dagster/Argo

## What to focus for the logging
For an LLM, you should log:
Requests & Responses: Input prompts, model predictions, confidence
Latency & Performance Metrics: How long inference takes
Errors & Exceptions: Any failures in model serving, request timeouts.
User Feedback (if applicable): User ratings or corrections to detect bad responses.
Token Usage: Number of tokens per request.
Data Distribution: Track changes in the type of data (distribution) the model is processing. Last 3 points could be useful to detect data/model drift

With Grafana:
Visualize metrics from Prometheus (LLM response time, API errors).
Display logs from Loki (structured logs, request details).
Set alerts (e.g., notify if the model response time is slow)?

## Tests coverage report
![Tests coverage report](docs/img/tests-coverage-report.png)
