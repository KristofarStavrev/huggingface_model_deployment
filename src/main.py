from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from model_utils import ModelHandler

app = FastAPI()

# Initialize the model handler
model_handler = ModelHandler(model_name="distilbert-base-uncased", adapter_name="Krython/lora_fine_tune_experiment")


# Define a Pydantic model for input validation
class PredictionRequest(BaseModel):
    text: str


@app.get("/")
def root():
    """
    Root endpoint that returns a welcome message.
    """

    return {"message": "Welcome to the sentiment analysis API!"}


@app.post("/predict")
def predict(request: PredictionRequest):
    """
    Endpoint for sentiment prediction.
    Accepts a text input and returns the prediction.
    """

    try:
        prediction = model_handler.predict(request.text)
        return {"text": request.text, "prediction": prediction}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")
