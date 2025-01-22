import pytest
from bullet.client import Numbers
from bullet import colors
from unittest.mock import patch


def test_numbers_initialization():
    """
    Test the initialization of the Numbers class.

    This test verifies that the Numbers class is correctly initialized with the
    provided parameters. It checks the following attributes:
    - prompt: The prompt message to be displayed.
    - indent: The number of spaces to indent the prompt.
    - word_color: The color of the prompt text.
    - type: The expected type of the input value.

    Assertions:
    - The prompt attribute should be "Enter a number:".
    - The indent attribute should be 4.
    - The word_color attribute should be the color blue from the colors.foreground dictionary.
    - The type attribute should be int.
    """
    numbers_prompt = Numbers(prompt="Enter a number:", indent=4, word_color=colors.foreground["blue"], type=int)
    assert numbers_prompt.prompt == "Enter a number:"
    assert numbers_prompt.indent == 4
    assert numbers_prompt.word_color == colors.foreground["blue"]
    assert numbers_prompt.type is int


def test_numbers_empty_prompt():
    """
    Test that the Numbers class raises a ValueError when initialized with an empty prompt.

    This test ensures that the Numbers class correctly handles the case where an empty
    string is provided as the prompt, raising a ValueError with the appropriate error message.

    Raises:
        ValueError: If the prompt is an empty string, with the message "Prompt can not be empty!".
    """
    with pytest.raises(ValueError, match="Prompt can not be empty!"):
        Numbers(prompt="")


def test_numbers_valid():
    """
    Test the validity of number inputs for the Numbers prompt.

    This function tests the `valid` method of the `Numbers` class to ensure
    that it correctly identifies valid and invalid number inputs.

    Assertions:
        - The string "123" is a valid number input and should return True.
        - The string "abc" is an invalid number input and should return False.
    """
    numbers_prompt = Numbers(prompt="Enter a number:", type=int)
    assert numbers_prompt.valid("123") is True
    assert numbers_prompt.valid("abc") is False


def test_numbers_launch_with_default(mocker):
    """
    Test the Numbers prompt launch with a default value.

    This test verifies that the Numbers prompt correctly launches with a default value
    and returns the expected result when user input is provided. It also checks that
    the forceWrite utility function is called at least once during the process.

    Args:
        mocker: The mocker fixture provided by pytest-mock for creating mock objects.

    Patches:
        bullet.utils.forceWrite: Mocked to track the number of times it is called.
        bullet.client.myInput.input: Mocked to simulate user input of "42".

    Asserts:
        The result of the Numbers prompt launch is 42.
        The forceWrite function is called more than 0 times.
    """
    numbers_prompt = Numbers(prompt="Enter a number:", type=int)

    with patch("bullet.utils.forceWrite") as mock_forceWrite, patch("bullet.client.myInput.input", return_value="42"):
        result = numbers_prompt.launch(default=0)

        assert result == 42
        assert mock_forceWrite.call_count > 0


def test_numbers_launch_invalid_default():
    """
    Test case for the Numbers class to ensure that providing an invalid default value
    raises a ValueError.

    This test verifies that when the `launch` method is called with a `default` value
    that is not of type `int`, a ValueError is raised with the appropriate error message.

    Steps:
    1. Create an instance of the Numbers class with a prompt and type set to int.
    2. Use pytest to assert that a ValueError is raised when `launch` is called with
        a `default` value of "invalid" (a string).

    Expected Result:
    A ValueError is raised with the message "`default` should be a <class 'int'>".
    """
    numbers_prompt = Numbers(prompt="Enter a number:", type=int)

    with pytest.raises(ValueError, match="`default` should be a <class 'int'>"):
        numbers_prompt.launch(default="invalid")


def test_numbers_launch_no_default(mocker):
    """
    Test the Numbers class launch method without a default value.

    This test verifies that the Numbers prompt correctly handles user input
    and returns the expected integer value. It also checks that the forceWrite
    function is called at least once.

    Args:
        mocker: The mocker fixture provided by pytest-mock for patching.

    Patches:
        bullet.utils.forceWrite: Mocked to verify call count.
        bullet.client.myInput.input: Mocked to return "42" as user input.

    Asserts:
        The result of the Numbers prompt launch method is 42.
        The forceWrite function is called more than 0 times.
    """
    numbers_prompt = Numbers(prompt="Enter a number:", type=int)

    # fmt: off
    with patch("bullet.utils.forceWrite") as mock_forceWrite, \
         patch("bullet.client.myInput.input", return_value="42"):
         # fmt: on

        result = numbers_prompt.launch()

        assert result == 42
        assert mock_forceWrite.call_count > 0
