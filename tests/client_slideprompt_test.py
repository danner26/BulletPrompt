import pytest
from bullet.client import SlidePrompt
from unittest.mock import patch, MagicMock


def test_slideprompt_initialization():
    """
    Test the initialization of the SlidePrompt class.

    This test verifies that the SlidePrompt object is correctly initialized with the given components.
    It checks that the components list is set correctly, the initial index is set to 0, and the result list is initialized as empty.

    Assertions:
        - The components attribute of the SlidePrompt instance should match the provided mock_component.
        - The idx attribute should be initialized to 0.
        - The result attribute should be an empty list.
    """
    mock_component = MagicMock()
    mock_component.prompt = "Enter your name:"
    slide_prompt = SlidePrompt(components=[mock_component])
    assert slide_prompt.components == [mock_component]
    assert slide_prompt.idx == 0
    assert slide_prompt.result == []


def test_slideprompt_empty_components():
    """
    Test that SlidePrompt raises a ValueError when initialized with empty components.

    This test ensures that the SlidePrompt class correctly handles the case where
    it is given an empty list of components. It expects a ValueError to be raised
    with the message "Prompt components cannot be empty!".

    Raises:
        ValueError: If the components list is empty.
    """
    with pytest.raises(ValueError, match="Prompt components cannot be empty!"):
        SlidePrompt(components=[])


def test_slideprompt_summarize(mocker):
    """
    Test the summarize method of the SlidePrompt class.

    This test creates a mock component with a prompt and a result, then patches
    the built-in print function to verify that the summarize method of the
    SlidePrompt class correctly prints the prompt and result.

    Args:
        mocker: A pytest-mock fixture used to patch the print function.
    """
    mock_component = MagicMock()
    mock_component.prompt = "Enter your name:"
    slide_prompt = SlidePrompt(components=[mock_component])
    slide_prompt.result = [("Enter your name:", "John Doe")]

    mocker.patch("builtins.print")
    slide_prompt.summarize()
    print.assert_called_with("Enter your name:", "John Doe")


def test_slideprompt_launch(mocker):
    """
    Test the launch method of the SlidePrompt class.

    This test verifies that the SlidePrompt correctly launches its components and returns the expected results.
    It mocks the Bullet and Check components, simulates their behavior, and checks the final output of the SlidePrompt.

    Args:
        mocker: The mocker fixture used to create mock objects.

    Asserts:
        - The result of the SlidePrompt launch is as expected.
        - The clearConsoleUp function is called twice.
        - The moveCursorDown function is called twice.
    """
    mock_bullet = MagicMock()
    mock_bullet.prompt = "Select an option:"
    mock_bullet.launch.return_value = "Option 1"
    mock_bullet.shift = 1
    mock_bullet.choices = ["Option 1", "Option 2"]

    mock_check = MagicMock()
    mock_check.prompt = "Select multiple options:"
    mock_check.launch.return_value = ["Option 1"]
    mock_check.shift = 1
    mock_check.choices = ["Option 1", "Option 2"]

    slide_prompt = SlidePrompt(components=[mock_bullet, mock_check])

    with patch("bullet.utils.clearConsoleUp") as mock_clearConsoleUp, patch(
        "bullet.utils.moveCursorDown"
    ) as mock_moveCursorDown:
        result = slide_prompt.launch()

        assert result == [("Select an option:", "Option 1"), ("Select multiple options:", ["Option 1"])]
        assert mock_clearConsoleUp.call_count == 2
        assert mock_moveCursorDown.call_count == 2


def test_slideprompt_launch_without_bullet_or_check(mocker):
    """
    Test the SlidePrompt launch method without bullet or check components.

    This test uses the `mocker` fixture to create a mock component with a prompt and a return value.
    It then creates a `SlidePrompt` instance with the mock component and patches the `clearConsoleUp`
    and `moveCursorDown` functions from the `bullet.utils` module.

    The test verifies that:
    - The `launch` method of `SlidePrompt` returns the expected result.
    - The `clearConsoleUp` function is called once.
    - The `moveCursorDown` function is called once.

    Args:
        mocker (pytest_mock.plugin.MockerFixture): The mocker fixture for creating mock objects.
    """
    mock_component = MagicMock()
    mock_component.prompt = "Enter your name:"
    mock_component.launch.return_value = "John Doe"

    slide_prompt = SlidePrompt(components=[mock_component])

    # fmt: off
    with patch("bullet.utils.clearConsoleUp") as mock_clearConsoleUp, \
         patch("bullet.utils.moveCursorDown") as mock_moveCursorDown:
         # fmt: on
        result = slide_prompt.launch()

        assert result == [("Enter your name:", "John Doe")]
        assert mock_clearConsoleUp.call_count == 1
        assert mock_moveCursorDown.call_count == 1
