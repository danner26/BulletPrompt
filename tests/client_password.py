import pytest
from bullet.client import Password
from bullet import colors
from unittest.mock import patch


def test_password_initialization():
    password_prompt = Password(
        prompt="Enter your password:", indent=4, hidden="*", word_color=colors.foreground["blue"]
    )
    assert password_prompt.prompt == "Enter your password:"
    assert password_prompt.indent == 4
    assert password_prompt.hidden == "*"
    assert password_prompt.word_color == colors.foreground["blue"]


def test_password_empty_prompt():
    with pytest.raises(ValueError, match="Prompt can not be empty!"):
        Password(prompt="")


def test_password_launch(mocker):
    password_prompt = Password(prompt="Enter your password:", hidden="*")

    with patch("bullet.utils.forceWrite") as mock_forceWrite, patch(
        "bullet.client.myInput.input", return_value="my_secret_password"
    ):
        result = password_prompt.launch()

        assert result == "my_secret_password"
        assert mock_forceWrite.call_count > 0
