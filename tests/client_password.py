import pytest
from bullet.client import Password
from bullet import colors
from unittest.mock import patch


def test_password_initialization():
    """
    Test the initialization of the Password class.

    This test verifies that the Password class is correctly initialized with the
    provided prompt, indent, hidden character, and word color.

    Assertions:
        - The prompt attribute should be set to "Enter your password:".
        - The indent attribute should be set to 4.
        - The hidden attribute should be set to "*".
        - The word_color attribute should be set to colors.foreground["blue"].
    """
    password_prompt = Password(
        prompt="Enter your password:", indent=4, hidden="*", word_color=colors.foreground["blue"]
    )
    assert password_prompt.prompt == "Enter your password:"
    assert password_prompt.indent == 4
    assert password_prompt.hidden == "*"
    assert password_prompt.word_color == colors.foreground["blue"]


def test_password_empty_prompt():
    """
    Test that a ValueError is raised when an empty prompt is passed to the Password class.

    This test ensures that the Password class correctly handles the case where an
    empty prompt is provided by raising a ValueError with the appropriate error message.

    Raises:
        ValueError: If the prompt is empty, with the message "Prompt can not be empty!".
    """
    with pytest.raises(ValueError, match="Prompt can not be empty!"):
        Password(prompt="")


def test_password_launch(mocker):
    """
    Test the password prompt launch functionality.

    This test uses the `mocker` fixture to patch the `forceWrite` function and the `input` function
    from the `bullet.client.myInput` module. It simulates a user entering a password and verifies
    that the password prompt correctly captures and returns the entered password. Additionally,
    it checks that the `forceWrite` function is called at least once.

    Args:
        mocker: The mocker fixture used to patch functions.

    Asserts:
        The result of the password prompt launch is equal to the simulated user input.
        The `forceWrite` function is called at least once.
    """
    password_prompt = Password(prompt="Enter your password:", hidden="*")

    # fmt: off
    with patch("bullet.utils.forceWrite") as mock_forceWrite, \
         patch("bullet.client.myInput.input", return_value="my_secret_password"):
         # fmt: on
        result = password_prompt.launch()

        assert result == "my_secret_password"
        assert mock_forceWrite.call_count > 0
