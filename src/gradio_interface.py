import gradio as gr
import requests


class SentimentAnalysisAppUI:
    """
    Gradio interface for sentiment analysis using FastAPI.

    Args:
        api_url (str): The URL of the FastAPI endpoint.
        server_name (str): The server name to use for the Gradio interface.
        server_port (int): The server port to use for the Gradio interface.
        prevent_thread_lock (bool): Whether to prevent thread lock when launching the interface.

    Methods:
        sentiment_analysis: Sends a POST request to the FastAPI endpoint with the input text and returns the sentiment prediction.
        launch_gradio: Launches the Gradio interface.
    """

    def __init__(self, api_url="http://fastapi:8000/predict", server_name="0.0.0.0", server_port=7860, prevent_thread_lock=True): # nosec
        self.api_url = api_url
        self.server_name = server_name
        self.server_port = server_port
        self.prevent_thread_lock = prevent_thread_lock

        # Define Gradio interface with an improved layout
        with gr.Blocks(css=".gradio-container {max-width: 600px; margin: auto;}") as self.interface:
            gr.Markdown("<h2 style='text-align: center;'>🌟 Sentiment Analysis 🌟</h2>")
            gr.Markdown("<p style='text-align: center;'>Enter text below to analyze its sentiment.</p>")

            with gr.Row():
                self.input_text = gr.Textbox(label="Enter Text", placeholder="Type your text here...", lines=3)

            self.analyze_button = gr.Button("Analyze Sentiment")
            self.output_text = gr.Markdown()  # Markdown output for better formatting

            self.analyze_button.click(self.sentiment_analysis, inputs=self.input_text, outputs=self.output_text)

    def sentiment_analysis(self, text):
        """
        Sends a POST request to the FastAPI endpoint with the input text and returns the sentiment prediction.

        Args:
            text (str): The input text to analyze.

        Returns:
            str: The sentiment prediction or an error message.
        """
        response = requests.post(self.api_url, json={"text": text}, timeout=30)
        if response.status_code == 200:
            prediction = response.json().get("prediction", {})
            if isinstance(prediction, dict):
                # Extract scores and format them nicely
                pos = prediction.get("positive", 0) * 100
                neg = prediction.get("negative", 0) * 100
                return f"### Sentiment Scores:\n- **Positive:** {pos:.2f}%\n- **Negative:** {neg:.2f}%"
            return "Invalid prediction format"
        else:
            return f"❌ **Error:** {response.json().get('detail', 'Unknown error')}"

    def launch_gradio(self):
        """Launch Gradio interface."""
        self.interface.launch(server_name=self.server_name, server_port=self.server_port, prevent_thread_lock=self.prevent_thread_lock)


if __name__ == "__main__": # pragma: no cover
    app = SentimentAnalysisAppUI(prevent_thread_lock=False)
    app.launch_gradio()
