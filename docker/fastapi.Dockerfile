# Start with the official Python 3.10.12 image
FROM python:3.10.12-slim

ARG NEW_USER=sentimentapp
ARG HOME=/home/$NEW_USER
ARG POETRY_VERSION=2.0.1

USER root

# Install curl
RUN apt update && apt install -y curl && apt-get clean && rm -rf /var/lib/apt/lists/*

# Create new user
RUN groupadd -r $NEW_USER && useradd -r -g $NEW_USER -m $NEW_USER
USER $NEW_USER

# Install poetry - doing this first to cache dependencies before the rest of the project
RUN curl -sSL https://install.python-poetry.org | POETRY_VERSION=$POETRY_VERSION python3 -

# Add Poetry to the PATH (so you can call `poetry` inside the container)
ENV PATH="$HOME/.local/bin:${PATH}"

# Set the working directory
WORKDIR /app

# Copy the poetry configuration and lock files into the container
COPY pyproject.toml poetry.lock /app/

# Install the dependencies (package-mode already set to false in pyproject.toml)
RUN poetry install --without ui

# Copy the rest of the application code into the container
COPY src/main.py src/model_utils.py /app/

# Expose the ports for FastAPI and Gradio
EXPOSE 8000

# Run the app
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
