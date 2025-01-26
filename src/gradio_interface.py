import gradio as gr
import requests


class SentimentAnalysisAppUI:
    def __init__(self, api_url="http://127.0.0.1:8000/predict", server_name="0.0.0.0", server_port=7860):
        self.api_url = api_url
        self.server_name = server_name
        self.server_port = server_port

        # Define Gradio interface
        self.interface = gr.Interface(
            fn=self.sentiment_analysis,
            inputs="text",
            outputs="text",
            title="Sentiment Analysis",
            description="Enter a piece of text to get the sentiment prediction.",
            flagging_mode="never"
        )

    def sentiment_analysis(self, text):
        """
        Sends a POST request to the FastAPI endpoint with the input text and returns the sentiment prediction.

        Args:
            text (str): The input text to analyze.

        Returns:
            str: The sentiment prediction or an error message.
        """
        response = requests.post(self.api_url, json={"text": text})
        if response.status_code == 200:
            return response.json().get("prediction", "No prediction found")
        else:
            return f"Error: {response.json().get('detail', 'Unknown error')}"

    def launch_gradio(self):
        """Launch Gradio interface."""
        self.interface.launch(server_name=self.server_name, server_port=self.server_port, prevent_thread_lock=True)


# Usage example:
if __name__ == "__main__":
    app = SentimentAnalysisAppUI()
    app.launch_gradio()
