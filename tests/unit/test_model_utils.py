import pytest
from model_utils import ModelHandler
from peft import PeftModel


@pytest.fixture
def model_handler():
    """
    Fixture to initialize the ModelHandler class with the distilbert-base-uncased model
    and the Krython/lora_fine_tune_experiment adapter.
    """

    return ModelHandler(model_name="distilbert-base-uncased",
                        adapter_name="Krython/lora_fine_tune_experiment")


def test_model_initialization(model_handler):
    """
    Test the initialization of the ModelHandler class.
        - The tokenizer attribute should not be None.
        - The model attribute should not be None.
        - The model attribute should be an instance of the PeftModel class.
    """

    assert model_handler.tokenizer is not None
    assert model_handler.model is not None
    assert isinstance(model_handler.model, PeftModel)


def test_predict(model_handler):
    """
    Test the predict method of the Model with a sample input string.
        - The method should return a dictionary with the probabilities of the text being positive or negative.
        - The probabilities should be between 0 and 1.
        - The positive probability should be greater than the negative probability.
        - The positive probability should be greater than 0.5.
        - The negative probability should be less than 0.5.
    """

    text = "I love this movie!"
    prediction = model_handler.predict(text)
    assert "positive" in prediction
    assert "negative" in prediction
    assert isinstance(prediction["positive"], float)
    assert isinstance(prediction["negative"], float)
    assert 0 <= prediction["positive"] <= 1
    assert 0 <= prediction["negative"] <= 1
    assert prediction["positive"] > prediction["negative"]
    assert prediction["positive"] > 0.5
    assert prediction["negative"] < 0.5
