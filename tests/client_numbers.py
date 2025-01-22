import pytest
from bullet.client import Numbers
from bullet import colors
from unittest.mock import patch


def test_numbers_initialization():
    numbers_prompt = Numbers(prompt="Enter a number:", indent=4, word_color=colors.foreground["blue"], type=int)
    assert numbers_prompt.prompt == "Enter a number:"
    assert numbers_prompt.indent == 4
    assert numbers_prompt.word_color == colors.foreground["blue"]
    assert numbers_prompt.type is int


def test_numbers_empty_prompt():
    with pytest.raises(ValueError, match="Prompt can not be empty!"):
        Numbers(prompt="")


def test_numbers_valid():
    numbers_prompt = Numbers(prompt="Enter a number:", type=int)
    assert numbers_prompt.valid("123") is True
    assert numbers_prompt.valid("abc") is False


def test_numbers_launch_with_default(mocker):
    numbers_prompt = Numbers(prompt="Enter a number:", type=int)

    with patch("bullet.utils.forceWrite") as mock_forceWrite, patch("bullet.client.myInput.input", return_value="42"):
        result = numbers_prompt.launch(default=0)

        assert result == 42
        assert mock_forceWrite.call_count > 0


def test_numbers_launch_invalid_default():
    numbers_prompt = Numbers(prompt="Enter a number:", type=int)

    with pytest.raises(ValueError, match="`default` should be a <class 'int'>"):
        numbers_prompt.launch(default="invalid")


def test_numbers_launch_no_default(mocker):
    numbers_prompt = Numbers(prompt="Enter a number:", type=int)

    with patch("bullet.utils.forceWrite") as mock_forceWrite, patch("bullet.client.myInput.input", return_value="42"):
        result = numbers_prompt.launch()

        assert result == 42
        assert mock_forceWrite.call_count > 0
