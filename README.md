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
- [ ] Deploy in AWS - EC2 or ECS
- [ ] Terraform infrastructure
- [ ] Kubernetes/Kserve + GPU
- [ ] Linting
- [ ] Logging
- [ ] Prometheus, Grafana, Loki
- [ ] Training/Validation/Testing scripts and modularity
- [ ] Documentation (MkDocs / Sphinx) + Docstrings
- [ ] Pytest / doctest - unit/system tests
- [ ] Nox/Tox
- [ ] Mypy  - typechecking
- [ ] Model tracking, drift, automated retraining
- [ ] Airflow/Dagster/Argo
- [ ] After deployment - test out the CI/CD by creating a new feature branch, make some development changes, and merge with the master
- [ ] Create an diagram for the entire architecture (CI/CD, model retraining, etc.)
