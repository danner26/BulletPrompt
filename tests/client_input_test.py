import pytest
from bullet.client import Input
from bullet import colors
from unittest.mock import patch


def test_input_initialization():
    """
    Test the initialization of the Input class.

    This test verifies that the Input class is correctly initialized with the
    provided parameters and that its attributes are set as expected.

    Assertions:
        - The prompt attribute should be set to "Enter your name:".
        - The default attribute, excluding the first and last characters, should be "John Doe".
        - The indent attribute should be set to 4.
        - The word_color attribute should be set to the blue color from the colors.foreground dictionary.
        - The strip attribute should be set to True.
        - The pattern attribute should be set to the regular expression "^[a-zA-Z ]+$".
    """
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
    """
    Test case for Input class to ensure it raises a ValueError when an empty prompt is provided.

    This test verifies that the Input class correctly handles the case where an empty
    prompt string is passed, and raises a ValueError with the appropriate error message.

    Raises:
        ValueError: If the prompt is an empty string, with the message "Prompt can not be empty!".
    """
    with pytest.raises(ValueError, match="Prompt can not be empty!"):
        Input(prompt="")


def test_input_valid():
    """
    Test the validity of user input against a specified pattern.

    This test checks the `valid` method of the `Input` class to ensure it correctly
    validates input strings based on a given regular expression pattern.

    Assertions:
        - The input "John Doe" should be considered valid (contains only letters and spaces).
        - The input "12345" should be considered invalid (contains digits).

    Raises:
        AssertionError: If any of the assertions fail.
    """
    input_prompt = Input(prompt="Enter your name:", pattern="^[a-zA-Z ]+$")
    assert input_prompt.valid("John Doe") is True
    assert input_prompt.valid("12345") is False


def test_input_launch(mocker):
    """
    Test the launch method of the Input class.

    This test verifies that the launch method correctly processes user input
    by stripping whitespace and returning the expected result. It also checks
    that the forceWrite utility function is called at least once.

    Args:
        mocker: The mocker fixture provided by pytest-mock for creating mocks.

    Patches:
        - bullet.utils.forceWrite: Mocked to track call count.
        - bullet.client.myInput.input: Mocked to return a predefined input string.
        - input_prompt.valid: Mocked to always return True.

    Asserts:
        - The result of input_prompt.launch() is "John Doe".
        - The forceWrite function is called more than 0 times.
    """
    input_prompt = Input(prompt="Enter your name:", default="John Doe", strip=True)

    # fmt: off
    with patch("bullet.utils.forceWrite") as mock_forceWrite, \
         patch("bullet.client.myInput.input", return_value=" John Doe "), \
         patch.object(input_prompt, "valid", return_value=True):
         # fmt: on

        result = input_prompt.launch()

        assert result == "John Doe"
        assert mock_forceWrite.call_count > 0
