from fastapi import FastAPI
from src.model_utils import ModelHandler

app = FastAPI()

model_handler = ModelHandler("distilbert-base-uncased")

@app.get("/")
def root():
    return {"message": "Welcome to the sentiment analysis API!"}


@app.post("/predict")
def predict(request: str):
    prediction = model_handler.predict(request)
    return {"text": request, "prediction": prediction}
