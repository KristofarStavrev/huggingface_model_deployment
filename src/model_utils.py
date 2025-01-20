import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification


class ModelHandler():
    def __init__(self, model_name, adapter_name=None):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        self.model.eval()

    def predict(self, text):
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True).to(self.device)

        with torch.no_grad():
            outputs = self.model(**inputs)
        
        probs = torch.nn.functional.softmax(outputs.logits, dim=1)

        return {
            "positive": float(probs[0][1]),
            "negative": float(probs[0][0])
        }
