import gradio as gr
import requests
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


class SentimentAnalysisAppUI:
    """
    Gradio interface for sentiment analysis using FastAPI.

    Args:
        api_url (str): The URL of the FastAPI endpoint.
        server_name (str): The server name to use for the Gradio interface.
        server_port (int): The server port to use for the Gradio interface.
        root_path (str): The root path for the Gradio interface (mainly used for ingress later on).
        prevent_thread_lock (bool): Whether to prevent thread lock when launching the interface.

    Methods:
        sentiment_analysis: Sends a POST request to the FastAPI endpoint with the input text and returns the sentiment prediction.
        launch_gradio: Launches the Gradio interface.
    """

    def __init__(self, api_url: str = os.getenv("FASTAPI_URL", "http://fastapi-service:8000/predict"),
                 server_name: str = "0.0.0.0",
                 server_port: int = 7860,
                 root_path: str = "/ui",
                 prevent_thread_lock: bool = True):  # nosec

        self.api_url = api_url
        self.server_name = server_name
        self.server_port = server_port
        self.root_path = root_path
        self.prevent_thread_lock = prevent_thread_lock

        logger.info("Initializing Gradio interface...")

        # Define Gradio interface with an improved layout
        with gr.Blocks(css=".gradio-container {max-width: 600px; margin: auto;}") as self.interface:
            gr.Markdown("<h2 style='text-align: center;'>🌟 Sentiment Analysis 🌟</h2>")
            gr.Markdown("<p style='text-align: center;'>Enter text below to analyze its sentiment.</p>")

            with gr.Row():
                self.input_text = gr.Textbox(label="Enter Text", placeholder="Type your text here...", lines=3)

            self.analyze_button = gr.Button("Analyze Sentiment")
            self.output_text = gr.Markdown()

            self.analyze_button.click(self.sentiment_analysis,
                                      inputs=self.input_text,
                                      outputs=self.output_text)

        logger.info("Gradio interface initialized.")

    def sentiment_analysis(self, text: str) -> str:
        """
        Sends a POST request to the FastAPI endpoint with the input text and returns the sentiment prediction.

        Args:
            text (str): The input text to analyze.

        Returns:
            str: The sentiment prediction or an error message.
        """

        logger.info(f"Sending request to fastAPI: {text}")
        response = requests.post(self.api_url, json={"text": text}, timeout=30)
        if response.status_code == 200:
            prediction = response.json().get("prediction", {})
            if isinstance(prediction, dict):
                # Extract scores and format them nicely
                pos = prediction.get("positive", 0) * 100
                neg = prediction.get("negative", 0) * 100
                logger.info(f"API request successful, received prediction: {prediction}")
                return f"### Sentiment Scores:\n- **Positive:** {pos:.2f}%\n- **Negative:** {neg:.2f}%"
            return "Invalid prediction format"
        else:
            logger.error(f"API request failed: {response.status_code} - {response.text}")
            return f"❌ **Error:** {response.json().get('detail', 'Unknown error')}"

    def launch_gradio(self) -> None:
        """Launch Gradio interface."""
        logger.info("Launching Gradio interface...")
        self.interface.launch(server_name=self.server_name,
                              server_port=self.server_port,
                              root_path=self.root_path,
                              prevent_thread_lock=self.prevent_thread_lock)


if __name__ == "__main__":  # pragma: no cover
    app = SentimentAnalysisAppUI(prevent_thread_lock=False)
    app.launch_gradio()
