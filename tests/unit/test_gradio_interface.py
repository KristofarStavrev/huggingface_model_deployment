# import pytest
# import requests
# from gradio_interface import SentimentAnalysisAppUI

# @pytest.fixture
# def gradio_app():
#     return SentimentAnalysisAppUI(api_url="http://testserver/predict")

# def test_sentiment_analysis_success(mocker, gradio_app):
#     mock_response = mocker.Mock()
#     mock_response.status_code = 200
#     mock_response.json.return_value = {"prediction": {"positive": 0.8, "negative": 0.2}}
#     mocker.patch("requests.post", return_value=mock_response)

#     result = gradio_app.sentiment_analysis("Great movie!")
#     assert "**Positive:** 80.00%" in result

# def test_sentiment_analysis_error(mocker, gradio_app):
#     mock_response = mocker.Mock()
#     mock_response.status_code = 500
#     mock_response.json.return_value = {"detail": "Internal server error"}
#     mocker.patch("requests.post", return_value=mock_response)

#     result = gradio_app.sentiment_analysis("Bad movie!")
#     assert "❌ **Error:** Internal server error" in result
