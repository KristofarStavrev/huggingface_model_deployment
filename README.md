# huggingface_model_deployment

## TODO:
- [X] Upload model to HuggingFace modelhub
- [X] Productionize and modularize code
- [X] Dockerize
    - [X] Integrate poetry
    - [X] Separate the fastAPI backend and gradio frontend services in different containers
    - [X] Handle them with Docker compose
- [X] Makefile
- [IN PROGRESS] CI/CD - GitHub actions free tier
- [ ] Pytest / doctest - unit/system tests
- [ ] Nox/Tox
- [ ] Mypy  - typechecking
- [ ] Linting
- [ ] Logging
- [ ] Prometheus, Grafana, Loki
- [ ] Training/Validation/Testing scripts and modularity
- [ ] Documentation (MkDocs / Sphinx) + Docstrings
- [ ] Kubernetes/Kserve/Helmchart + GPU
- [ ] Model tracking, drift, automated retraining
- [ ] Airflow/Dagster/Argo
- [ ] Create an diagram for the entire architecture (CI/CD, model retraining, etc.)
- [ ] OPTIONAL: Deploy in AWS - EC2 or ECS
- [ ] OPTIONAL: Terraform infrastructure
