from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200


def test_predict_valid():
    response = client.post("/predict", json={"text": "I love this movie!"})
    assert response.status_code == 200
    assert "prediction" in response.json()


def test_predict_invalid_missing():
    response = client.post("/predict", json={})
    assert response.status_code == 422


def test_predict_invalid_numeric():
    response = client.post("/predict", json={"text": 123})
    assert response.status_code == 422


def test_predict_internal_error(mocker):
    mocker.patch("model_utils.ModelHandler.predict", side_effect=Exception("Mocked error"))
    response = client.post("/predict", json={"text": "Test"})
    assert response.status_code == 500
    assert "Prediction error" in response.json()["detail"]
