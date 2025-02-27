# Outdated since the project has been migrated to Docker Compose
DOCKERFILE = docker/Dockerfile
IMAGE_NAME = llm_movie_sentiment_app
IMAGE_TAG ?= latest
CONTAINER_NAME = sentiment_app_container

# Build Docker image
build:
	docker build -t $(IMAGE_NAME):$(IMAGE_TAG) -f $(DOCKERFILE) .

# Run Docker container
run:
	docker run -d -p 8000:8000 -p 7860:7860 --name $(CONTAINER_NAME) $(IMAGE_NAME):$(IMAGE_TAG)

# Stop all running containers
stop-all:
	docker stop $(shell docker ps -q)

# Remove all stopped containers
remove-containers:
	docker rm $(shell docker ps -a -q)

# Remove all images
remove-images:
	docker rmi $(shell docker images -q)

# Clean Docker cache (unused images, volumes, networks, etc.)
clean-cache:
	docker system prune -f

# Stop all containers, remove all containers, remove all images, and clean cache
docker-full-clean: stop-all remove-containers remove-images clean-cache

# Stop all containers, remove all containers, remove all images, and clean cache
docker-partial-clean: remove-images clean-cache

run-pytests:
	poetry run pytest tests/unit/ -v

run-pytests-coverage:
	poetry run pytest --cov=src tests/unit/ -v

run-pytests-coverage-html:
	poetry run pytest --cov=src --cov-report=html tests/unit/ -v
