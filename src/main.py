from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from model_utils import ModelHandler
from typing import Union
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST, Histogram, Gauge
from starlette.responses import Response
import logging
import sys
import os
import time

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


# Metric for Prometheus
ROOT_REQUEST = Counter("root_requests_total", "Total number of root requests")
PREDICT_REQUESTS = Counter('predict_requests_total', 'Total number of POST requests to the /predict endpoint')
PREDICT_SUCCESSES = Counter("predict_success_total", "Total number of successful predictions")
PREDICT_FAILURES = Counter("predict_failure_total", "Total number of failed predictions")
PREDICT_INFERENCE_DURATION = Histogram(
    "predict_inference_duration_seconds",
    "Time spent performing inference in the /predict endpoint",
    buckets=[0.005, 0.01, 0.015, 0.0175, 0.02, 0.0225, 0.025, 0.0275, 0.03,
             0.04, 0.05, 0.075, 0.1, 0.15, 0.2, 0.25, 0.5, 1.0, 2.0, 5.0, 10.0]
)
USER_INPUT_WORDS_LENGTH = Histogram(
    "user_input_word_length",
    "Length of user input (in words)",
    buckets=[1, 5, 10, 20, 50, 100, 200, 500, 1000, 2000]
)

# Counter for prediction labels
PREDICTION_LABEL_COUNTER = Counter(
    "prediction_label_total",
    "Count of predictions by label",
    ["label"]
)

# Histogram for confidence score distribution
PREDICTION_CONFIDENCE_HISTOGRAM = Histogram(
    "prediction_confidence",
    "Confidence scores of predictions",
    ["label"],  # Separate histogram per class (optional, but insightful)
    buckets=[i * 0.1 for i in range(11)]  # 0.0 to 1.0 in steps of 0.1
)

LAST_CONFIDENCE = Gauge("last_prediction_confidence", "Confidence of the last prediction")

@app.get("/")
def root() -> dict[str, str]:
    """
    Root endpoint that returns a welcome message.
    """

    logger.info("Root endpoint accessed")
    ROOT_REQUEST.inc()

    return {"message": "Welcome to the sentiment analysis API!"}


@app.post("/predict")
def predict(request: PredictionRequest) -> dict[str, Union[str, dict]]:
    """
    Endpoint for sentiment prediction.
    Accepts a text input and returns the prediction.
    """

    PREDICT_REQUESTS.inc()
    logger.info(f"Prediction request received: {request.text}")

    input_length = len(request.text.split())
    USER_INPUT_WORDS_LENGTH.observe(input_length)

    start_time = time.perf_counter()

    try:
        with PREDICT_INFERENCE_DURATION.time():
            prediction = model_handler.predict(request.text)

        duration = time.perf_counter() - start_time
        logger.info(f"Prediction successful in {duration:.4f} seconds: {prediction}")

        PREDICT_SUCCESSES.inc()

        # Extract the label with highest confidence
        label = "positive" if prediction["positive"] >= prediction["negative"] else "negative"
        confidence = prediction[label]

        # Update metrics
        PREDICTION_LABEL_COUNTER.labels(label=label).inc()
        PREDICTION_CONFIDENCE_HISTOGRAM.labels(label=label).observe(confidence)
        LAST_CONFIDENCE.set(confidence)

        return {"text": request.text, "prediction": prediction}

    except Exception:
        duration = time.perf_counter() - start_time
        logger.error(f"Prediction failed after {duration:.4f} seconds", exc_info=True)
        PREDICT_FAILURES.inc()
        raise HTTPException(status_code=500, detail="Internal server error during prediction.")


@app.get("/metrics")
def metrics(credentials: HTTPBasicCredentials = Depends(authenticate)):
    """
    Endpoint for metrics scraped by prometheus.
    """

    data = generate_latest()
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)
