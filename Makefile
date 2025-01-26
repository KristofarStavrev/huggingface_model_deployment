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
remove-all:
	docker rm $(shell docker ps -a -q)

# Remove all images
clean-all-images:
	docker rmi $(shell docker images -q)

# Clean Docker cache (unused images, volumes, networks, etc.)
clean-cache:
	docker system prune -f

# Stop all containers, remove all containers, remove all images, and clean cache
docker-full-clean: stop-all remove-all clean-all-images clean-cache
