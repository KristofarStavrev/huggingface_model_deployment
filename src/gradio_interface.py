import gradio as gr
import requests


# Gradio prediction function
def sentiment_analysis(text):
    api_url = "http://127.0.0.1:8000/predict"  # Your FastAPI endpoint
    response = requests.post(api_url, json={"text": text})
    if response.status_code == 200:
        return response.json()["prediction"]
    else:
        return f"Error: {response.json()['detail']}"


# Gradio interface
interface = gr.Interface(
    fn=sentiment_analysis,
    inputs="text",
    outputs="text",
    title="Sentiment Analysis",
    description="Enter a piece of text to get the sentiment prediction."
)

if __name__ == "__main__":
    interface.launch()
