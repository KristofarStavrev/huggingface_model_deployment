# Start with the official Python 3.10.12 image
FROM python:3.10.12-slim

ARG POETRY_VERSION=2.0.1

# Set the working directory
WORKDIR /app

# Install poetry - doing this first to cache dependencies before the rest of the project
RUN curl -sSL https://install.python-poetry.org | POETRY_VERSION=$POETRY_VERSION python3 -

# Add Poetry to the PATH (so you can call `poetry` inside the container)
ENV PATH="/root/.local/bin:${PATH}"

# Copy the poetry configuration and lock files into the container
COPY pyproject.toml poetry.lock /app/

# Install the dependencies (package-mode already set to false in pyproject.toml)
RUN poetry install

# Copy the rest of the application code into the container
COPY src /app/

# Expose port
EXPOSE 80

# Run the app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
