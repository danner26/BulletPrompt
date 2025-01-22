import pytest
from bullet.client import VerticalPrompt
from bullet import colors
from unittest.mock import patch, MagicMock


def test_verticalprompt_initialization():
    """
    Test the initialization of the VerticalPrompt class.

    This test verifies that the VerticalPrompt class is correctly initialized with the provided components, spacing, separator, and separator color. It also checks that the separator length is set to the length of the prompt of the first component.

    Assertions:
        - The components attribute of the VerticalPrompt instance should match the provided components.
        - The spacing attribute should match the provided spacing value.
        - The separator attribute should match the provided separator value.
        - The separator_color attribute should match the provided separator color.
        - The separator_len attribute should be equal to the length of the prompt of the first component.
    """
    mock_component = MagicMock()
    mock_component.prompt = "Enter your name:"
    vertical_prompt = VerticalPrompt(
        components=[mock_component], spacing=2, separator="-", separator_color=colors.foreground["blue"]
    )
    assert vertical_prompt.components == [mock_component]
    assert vertical_prompt.spacing == 2
    assert vertical_prompt.separator == "-"
    assert vertical_prompt.separator_color == colors.foreground["blue"]
    assert vertical_prompt.separator_len == len(mock_component.prompt)


def test_verticalprompt_empty_components():
    """
    Test that VerticalPrompt raises a ValueError when initialized with empty components.

    This test ensures that the VerticalPrompt class correctly handles the case where
    an empty list of components is provided, raising a ValueError with the appropriate
    error message.

    Raises:
        ValueError: If the components list is empty, with the message "Prompt components cannot be empty!".
    """
    with pytest.raises(ValueError, match="Prompt components cannot be empty!"):
        VerticalPrompt(components=[])


def test_verticalprompt_summarize(mocker):
    """
    Test the summarize method of the VerticalPrompt class.

    This test creates a mock component with a prompt and a corresponding result.
    It then patches the built-in print function to verify that the summarize method
    of the VerticalPrompt class correctly prints the prompt and result.

    Args:
        mocker: A pytest-mock fixture that allows for mocking and patching.
    """
    mock_component = MagicMock()
    mock_component.prompt = "Enter your name:"
    vertical_prompt = VerticalPrompt(components=[mock_component])
    vertical_prompt.result = [("Enter your name:", "John Doe")]

    mocker.patch("builtins.print")
    vertical_prompt.summarize()
    print.assert_called_with("Enter your name:", "John Doe")


def test_verticalprompt_launch_with_separator(mocker):
    """
    Test the launch method of the VerticalPrompt class with a separator.

    This test verifies that the VerticalPrompt class correctly launches with a
    separator and returns the expected result. It mocks a component with a prompt
    and a return value, then checks if the launch method returns the correct
    prompt-response pair. Additionally, it ensures that the separator is printed
    correctly using the cprint function.

    Args:
        mocker (pytest_mock.plugin.MockerFixture): The mocker fixture for creating
        mock objects.

    Asserts:
        The result of the launch method is a list containing a tuple with the
        prompt and the response.
        The cprint function is called with the correct separator string and color.
    """
    mock_component = MagicMock()
    mock_component.prompt = "Enter your name:"
    mock_component.launch.return_value = "John Doe"
    vertical_prompt = VerticalPrompt(components=[mock_component], separator="-")

    with patch("bullet.utils.cprint") as mock_cprint:
        result = vertical_prompt.launch()
        assert result == [("Enter your name:", "John Doe")]
        mock_cprint.assert_called_with("-" * vertical_prompt.separator_len, color=vertical_prompt.separator_color)


def test_verticalprompt_launch_without_separator(mocker):
    """
    Test the `VerticalPrompt` class's `launch` method without a separator.

    This test verifies that the `VerticalPrompt` class can correctly launch a prompt
    with a specified spacing between components and return the expected result.

    Args:
        mocker (pytest_mock.plugin.MockerFixture): The mocker fixture for creating mocks.

    Test Steps:
    1. Create a mock component with a prompt and a return value.
    2. Instantiate a `VerticalPrompt` object with the mock component and a specified spacing.
    3. Patch the `bullet.utils.forceWrite` method to monitor its calls.
    4. Call the `launch` method of the `VerticalPrompt` instance.
    5. Assert that the result of the `launch` method is as expected.
    6. Verify that the `forceWrite` method was called with the correct spacing.

    Asserts:
        - The result of the `launch` method should be a list containing a tuple with the prompt and the return value.
        - The `forceWrite` method should be called with the correct number of newline characters based on the specified spacing.
    """
    mock_component = MagicMock()
    mock_component.prompt = "Enter your name:"
    mock_component.launch.return_value = "John Doe"
    vertical_prompt = VerticalPrompt(components=[mock_component], spacing=2)

    with patch("bullet.utils.forceWrite") as mock_forceWrite:
        result = vertical_prompt.launch()
        assert result == [("Enter your name:", "John Doe")]
        mock_forceWrite.assert_called_with("\n" * vertical_prompt.spacing)
