import pytest
from fastapi.testclient import TestClient
from main import app
from gradio_interface import SentimentAnalysisAppUI


@pytest.fixture
def fastapi_client():
    """Fixture to initialize the FastAPI TestClient."""
    return TestClient(app)


@pytest.fixture
def gradio_app():
    """Fixture to initialize the Gradio app."""
    return SentimentAnalysisAppUI(api_url="http://testserver/predict")


def test_gradio_fastapi_integration(fastapi_client, gradio_app, mocker):
    """
    Test integration between Gradio and FastAPI.
    Ensures Gradio's sentiment_analysis method correctly interacts with FastAPI.
    """

    response = fastapi_client.post("/predict", json={"text": "I love this movie!"})
    
    assert response.status_code == 200
    assert "prediction" in response.json()

    mocker.patch("requests.post", side_effect=lambda url, json: fastapi_client.post("/predict", json=json))
    result = gradio_app.sentiment_analysis("I love this movie!")

    assert "**Positive:**" in result and "**Negative:**" in result
