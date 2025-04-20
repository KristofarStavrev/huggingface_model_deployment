from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_root():
    """
    Test the root endpoint. It should return a 200 status code.
    """
    response = client.get("/")
    assert response.status_code == 200


def test_predict_valid():
    """
    Test the predict endpoint with valid input. It should return a 200 status code and a prediction.
    """
    response = client.post("/predict", json={"text": "I love this movie!"})
    assert response.status_code == 200
    assert "prediction" in response.json()


def test_predict_invalid_missing():
    """
    Test the predict endpoint with missing input. It should return a 422 status code.
    """
    response = client.post("/predict", json={})
    assert response.status_code == 422


def test_predict_invalid_numeric():
    """
    Test the predict endpoint with invalid input (numeric). It should return a 422 status code.
    """
    response = client.post("/predict", json={"text": 123})
    assert response.status_code == 422


def test_predict_internal_error(mocker):
    """
    Test the predict endpoint with an internal error with a mocker. It should return a 500 status code.
    """
    mocker.patch("model_utils.ModelHandler.predict",
                 side_effect=Exception("Mocked error"))

    response = client.post("/predict", json={"text": "Test"})
    assert response.status_code == 500
    assert "Internal server error during prediction." in response.json()["detail"]
