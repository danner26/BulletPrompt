import pytest
from bullet.client import SlidePrompt
from unittest.mock import patch, MagicMock


def test_slideprompt_initialization():
    mock_component = MagicMock()
    mock_component.prompt = "Enter your name:"
    slide_prompt = SlidePrompt(components=[mock_component])
    assert slide_prompt.components == [mock_component]
    assert slide_prompt.idx == 0
    assert slide_prompt.result == []


def test_slideprompt_empty_components():
    with pytest.raises(ValueError, match="Prompt components cannot be empty!"):
        SlidePrompt(components=[])


def test_slideprompt_summarize(mocker):
    mock_component = MagicMock()
    mock_component.prompt = "Enter your name:"
    slide_prompt = SlidePrompt(components=[mock_component])
    slide_prompt.result = [("Enter your name:", "John Doe")]

    mocker.patch("builtins.print")
    slide_prompt.summarize()
    print.assert_called_with("Enter your name:", "John Doe")


def test_slideprompt_launch(mocker):
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
    mock_component = MagicMock()
    mock_component.prompt = "Enter your name:"
    mock_component.launch.return_value = "John Doe"

    slide_prompt = SlidePrompt(components=[mock_component])

    with patch("bullet.utils.clearConsoleUp") as mock_clearConsoleUp, patch(
        "bullet.utils.moveCursorDown"
    ) as mock_moveCursorDown:
        result = slide_prompt.launch()

        assert result == [("Enter your name:", "John Doe")]
        assert mock_clearConsoleUp.call_count == 1
        assert mock_moveCursorDown.call_count == 1
