import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from peft import PeftModel
from typing import Optional
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


class ModelHandler():
    """
    Class to handle the sentiment analysis model and tokenizer.

    Attributes:
        tokenizer (AutoTokenizer): The tokenizer for the model.
        model (AutoModelForSequenceClassification): The sentiment analysis model.
        device (torch.device): The device to run the model on (CPU or GPU).

    Methods:
        predict: Predicts the sentiment of the given text.
    """

    def __init__(self, model_name: str, adapter_name: Optional[str] = None):
        logger.info(f"Loading model: {model_name}")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        logger.info(f"Using device: {self.device}")

        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)

        # Load and apply the adapter if provided
        if adapter_name:
            logger.info(f"Loading adapter: {adapter_name}")
            self.model = PeftModel.from_pretrained(self.model, adapter_name)

        self.model.to(self.device)
        self.model.eval()
        logger.info("Model initialized successfully.")

    def predict(self, text: str) -> dict[str, float]:
        """
        Method to predict the sentiment of the given text.

        Args:
            text (str): The input text for sentiment analysis.

        Returns:
            dict: A dictionary with the probabilities of the text being positive or negative.
        """
        
        logger.info(f"Predicting sentiment for text: {text}")
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True).to(self.device)

        with torch.no_grad():
            outputs = self.model(**inputs)
        
        probs = torch.nn.functional.softmax(outputs.logits, dim=1)
        results = {
            "positive": float(probs[0][1]),
            "negative": float(probs[0][0])
        }

        return results
