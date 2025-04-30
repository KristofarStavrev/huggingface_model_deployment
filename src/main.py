from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from model_utils import ModelHandler
from typing import Union
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response
import logging
import sys
import os

# Set up the logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a console handler that sends logs to stdout
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(logging.Formatter('%(asctime)s | %(levelname)s | Custom Log | %(filename)s | %(message)s'))

# Add the handler to the logger
logger.addHandler(console_handler)

# Prevent propagation to root logger
logger.propagate = False

app = FastAPI()
logger.info("FastAPI is starting...")

# Authentication for the metrics endpoint for Prometheus
security = HTTPBasic()
USERNAME = os.getenv("PROMETHEUS_METRICS_USER")
PASSWORD = os.getenv("PROMETHEUS_METRICS_PASS")


def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != USERNAME or credentials.password != PASSWORD:
        raise HTTPException(status_code=401, detail="Unauthorized")


# Initialize the model handler
logger.info("Initializing model...")
model_handler = ModelHandler(model_name="distilbert-base-uncased",
                             adapter_name="Krython/lora_fine_tune_experiment")


# Define a Pydantic model for input validation
class PredictionRequest(BaseModel):
    text: str


# Metric to track the number of requests
REQUEST_COUNTER = Counter("app_requests_total", "Total number of requests")


@app.get("/")
def root() -> dict[str, str]:
    """
    Root endpoint that returns a welcome message.
    """

    logger.info("Root endpoint accessed")
    REQUEST_COUNTER.inc()

    return {"message": "Welcome to the sentiment analysis API!"}


@app.post("/predict")
def predict(request: PredictionRequest) -> dict[str, Union[str, dict]]:
    """
    Endpoint for sentiment prediction.
    Accepts a text input and returns the prediction.
    """

    logger.info(f"Prediction request received: {request.text}")

    try:
        prediction = model_handler.predict(request.text)
        logger.info(f"Prediction successful: {prediction}")
        return {"text": request.text, "prediction": prediction}
    except Exception:
        logger.error("Prediction error", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error during prediction.")


@app.get("/metrics")
def metrics(credentials: HTTPBasicCredentials = Depends(authenticate)):
    """
    Endpoint for metrics scraped by prometheus.
    """

    data = generate_latest()
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)
