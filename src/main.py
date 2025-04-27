from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from model_utils import ModelHandler
from typing import Union
import logging
import sys

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

# Initialize the model handler
logger.info("Initializing model...")
model_handler = ModelHandler(model_name="distilbert-base-uncased",
                             adapter_name="Krython/lora_fine_tune_experiment")


# Define a Pydantic model for input validation
class PredictionRequest(BaseModel):
    text: str


logging.info("FastAPI is starting...")


@app.get("/")
def root() -> dict[str, str]:
    """
    Root endpoint that returns a welcome message.
    """

    logger.info("Root endpoint accessed")

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
