from fastapi.testclient import TestClient
from main import app
from base64 import b64encode

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


def get_basic_auth_header(username: str, password: str) -> dict:
    token = b64encode(f"{username}:{password}".encode()).decode()
    return {"Authorization": f"Basic {token}"}


def test_metrics_endpoint_auth_success(mocker):
    mocker.patch("main.USERNAME", "admin")
    mocker.patch("main.PASSWORD", "secret")

    headers = get_basic_auth_header("admin", "secret")
    response = client.get("/metrics", headers=headers)
    assert response.status_code == 200
    assert b"root_requests_total" in response.content
    assert b"predict_requests_total" in response.content
    assert b"predict_success_total" in response.content
    assert b"predict_failure_total" in response.content
    assert b"predict_inference_duration_seconds" in response.content
    assert b"user_input_word_length" in response.content
    assert b"prediction_label_total" in response.content
    assert b"prediction_confidence" in response.content


def test_metrics_endpoint_auth_failure(mocker):
    mocker.patch("main.USERNAME", "admin")
    mocker.patch("main.PASSWORD", "secret")

    headers = get_basic_auth_header("admin", "wrong")
    response = client.get("/metrics", headers=headers)
    assert response.status_code == 401
    assert response.json() == {"detail": "Unauthorized"}


def test_metrics_endpoint_auth_empty(mocker):
    mocker.patch("main.USERNAME", "admin")
    mocker.patch("main.PASSWORD", "secret")

    response = client.get("/metrics")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}
