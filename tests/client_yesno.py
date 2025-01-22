import pytest
from bullet.client import YesNo
from bullet import colors
from unittest.mock import patch


def test_yesno_initialization():
    """
    Test the initialization of the YesNo class.

    This test verifies that the YesNo class is correctly initialized with the given parameters:
    - prompt: The question to be asked.
    - default: The default answer.
    - indent: The number of spaces to indent the prompt.
    - word_color: The color of the prompt text.
    - prompt_prefix: The prefix to be added before the prompt.

    Assertions:
    - The prompt should be correctly formatted with the prefix and question.
    - The default answer should be correctly formatted.
    - The indent should be set correctly.
    - The word color should be set correctly.
    """
    yesno = YesNo(
        prompt="Do you want to continue?",
        default="y",
        indent=4,
        word_color=colors.foreground["blue"],
        prompt_prefix="[y/n] ",
    )
    assert yesno.prompt == "[y/n] Do you want to continue?"
    assert yesno.default == "[y]"
    assert yesno.indent == 4
    assert yesno.word_color == colors.foreground["blue"]


def test_yesno_empty_prompt():
    """
    Test that YesNo raises a ValueError when initialized with an empty prompt.

    This test ensures that the YesNo class correctly handles the case where an
    empty prompt string is provided. It expects a ValueError to be raised with
    the message "Prompt can not be empty!".

    Raises:
        ValueError: If the prompt is an empty string.
    """
    with pytest.raises(ValueError, match="Prompt can not be empty!"):
        YesNo(prompt="")


def test_yesno_invalid_default():
    """
    Test case for the YesNo class to ensure that providing an invalid default value raises a ValueError.

    This test verifies that when an invalid default value (anything other than 'y' or 'n') is passed to the YesNo class,
    a ValueError is raised with the appropriate error message.

    Raises:
        ValueError: If the default value is not 'y' or 'n'.
    """
    with pytest.raises(ValueError, match="`default` can only be 'y' or 'n'!"):
        YesNo(prompt="Do you want to continue?", default="maybe")


def test_yesno_valid():
    """
    Test the `valid` method of the `YesNo` class.

    This test checks the following cases:
    - Valid inputs: "y", "n", "Y", "N", "yes", "no", "YES", "NO"
    - Invalid inputs: "maybe", None

    The `valid` method should return True for valid inputs and False for invalid inputs.
    """
    yesno = YesNo(prompt="Do you want to continue?")
    assert yesno.valid("y") is True
    assert yesno.valid("n") is True
    assert yesno.valid("Y") is True
    assert yesno.valid("N") is True
    assert yesno.valid("yes") is True
    assert yesno.valid("no") is True
    assert yesno.valid("YES") is True
    assert yesno.valid("NO") is True
    assert yesno.valid("maybe") is False
    assert yesno.valid(None) is False


def test_yesno_launch():
    """
    Test the launch method of the YesNo class.

    This test checks the following:
    - The YesNo instance is created with the prompt "Do you want to continue?".
    - The `forceWrite` function from `bullet.utils` is patched and its call count is checked.
    - The `valid` method of the YesNo instance is patched to return False on the first call and True on the second call.
    - The `input` function from `bullet.client.myInput` is patched to return "y".
    - The `launch` method of the YesNo instance is called and its result is asserted to be True.
    - The `forceWrite` function is called at least once.
    """
    yesno = YesNo(prompt="Do you want to continue?")

    # fmt: off
    with patch("bullet.utils.forceWrite") as mock_forceWrite, \
         patch.object(yesno, "valid", side_effect=[False, True]), \
         patch("bullet.client.myInput.input", return_value="y"):
         # fmt: on
        result = yesno.launch()

        assert result
        assert mock_forceWrite.call_count > 0
