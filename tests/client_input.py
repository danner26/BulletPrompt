import pytest
from bullet.client import Input
from bullet import colors
from unittest.mock import patch


def test_input_initialization():
    input_prompt = Input(
        prompt="Enter your name:",
        default="John Doe",
        indent=4,
        word_color=colors.foreground["blue"],
        strip=True,
        pattern="^[a-zA-Z ]+$",
    )
    assert input_prompt.prompt == "Enter your name:"
    assert input_prompt.default[1:-1] == "John Doe"
    assert input_prompt.indent == 4
    assert input_prompt.word_color == colors.foreground["blue"]
    assert input_prompt.strip is True
    assert input_prompt.pattern == "^[a-zA-Z ]+$"


def test_input_empty_prompt():
    with pytest.raises(ValueError, match="Prompt can not be empty!"):
        Input(prompt="")


def test_input_valid():
    input_prompt = Input(prompt="Enter your name:", pattern="^[a-zA-Z ]+$")
    assert input_prompt.valid("John Doe") is True
    assert input_prompt.valid("12345") is False


def test_input_launch(mocker):
    input_prompt = Input(prompt="Enter your name:", default="John Doe", strip=True)

    with patch("bullet.utils.forceWrite") as mock_forceWrite, patch(
        "bullet.client.myInput.input", return_value=" John Doe "
    ), patch.object(input_prompt, "valid", return_value=True):
        result = input_prompt.launch()

        assert result == "John Doe"
        assert mock_forceWrite.call_count > 0
