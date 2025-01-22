import pytest
from bullet.client import VerticalPrompt
from bullet import colors
from unittest.mock import patch, MagicMock


def test_verticalprompt_initialization():
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
    with pytest.raises(ValueError, match="Prompt components cannot be empty!"):
        VerticalPrompt(components=[])


def test_verticalprompt_summarize(mocker):
    mock_component = MagicMock()
    mock_component.prompt = "Enter your name:"
    vertical_prompt = VerticalPrompt(components=[mock_component])
    vertical_prompt.result = [("Enter your name:", "John Doe")]

    mocker.patch("builtins.print")
    vertical_prompt.summarize()
    print.assert_called_with("Enter your name:", "John Doe")


def test_verticalprompt_launch_with_separator(mocker):
    mock_component = MagicMock()
    mock_component.prompt = "Enter your name:"
    mock_component.launch.return_value = "John Doe"
    vertical_prompt = VerticalPrompt(components=[mock_component], separator="-")

    with patch("bullet.utils.cprint") as mock_cprint:
        result = vertical_prompt.launch()
        assert result == [("Enter your name:", "John Doe")]
        mock_cprint.assert_called_with("-" * vertical_prompt.separator_len, color=vertical_prompt.separator_color)


def test_verticalprompt_launch_without_separator(mocker):
    mock_component = MagicMock()
    mock_component.prompt = "Enter your name:"
    mock_component.launch.return_value = "John Doe"
    vertical_prompt = VerticalPrompt(components=[mock_component], spacing=2)

    with patch("bullet.utils.forceWrite") as mock_forceWrite:
        result = vertical_prompt.launch()
        assert result == [("Enter your name:", "John Doe")]
        mock_forceWrite.assert_called_with("\n" * vertical_prompt.spacing)
