import pytest
from gradio_interface import SentimentAnalysisAppUI


@pytest.fixture
def gradio_app():
    """Fixture to initialize the SentimentAnalysisAppUI class with a test server URL."""

    return SentimentAnalysisAppUI(api_url="http://testserver/predict")


def test_sentiment_analysis_success(mocker, gradio_app):
    """
    Test the sentiment_analysis method with a successful prediction.
    It should return the sentiment scores.
    """

    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"prediction": {"positive": 0.8, "negative": 0.2}}
    mocker.patch("requests.post", return_value=mock_response)

    result = gradio_app.sentiment_analysis("Great movie!")
    assert "**Positive:** 80.00%" in result
    assert "**Negative:** 20.00%" in result


def test_sentiment_analysis_error(mocker, gradio_app):
    """
    Test the sentiment_analysis method with an error response.
    It should return an error message.
    """

    mock_response = mocker.Mock()
    mock_response.status_code = 500
    mock_response.json.return_value = {"detail": "Internal server error"}
    mocker.patch("requests.post", return_value=mock_response)

    result = gradio_app.sentiment_analysis("Bad movie!")
    assert "❌ **Error:** Internal server error" in result


def test_invalid_prediction_format(mocker, gradio_app):
    """
    Test the sentiment_analysis method with an invalid prediction format.
    It should return an error message.
    """

    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"prediction": ["positive", 0.8, "negative", 0.2]}
    mocker.patch("requests.post", return_value=mock_response)

    result = gradio_app.sentiment_analysis("Strange movie!")
    assert result == "Invalid prediction format"


def test_launch_gradio(mocker, gradio_app):
    """
    Test the launch_gradio method. It should call the launch method from the Gradio interface.
    It should be called once.
    """

    mock_launch = mocker.patch.object(gradio_app.interface, "launch")
    gradio_app.launch_gradio()
    mock_launch.assert_called_once()
