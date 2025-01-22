import pytest
from bullet.client import ScrollBar
from bullet import colors, utils
from unittest.mock import patch


def test_scrollbar_initialization():
    scrollbar = ScrollBar(
        prompt="Select an option:",
        choices=["Option 1", "Option 2"],
        pointer="→",
        up_indicator="↑",
        down_indicator="↓",
        pointer_color=colors.foreground["red"],
        indicator_color=colors.foreground["blue"],
        word_color=colors.foreground["green"],
        word_on_switch=colors.REVERSE,
        background_color=colors.background["yellow"],
        background_on_switch=colors.REVERSE,
        pad_right=2,
        indent=4,
        align=2,
        margin=1,
        shift=1,
        height=5,
        return_index=True,
    )
    assert scrollbar.prompt == "Select an option:"
    assert scrollbar.choices == ["Option 1", "Option 2"]
    assert scrollbar.pointer == "→"
    assert scrollbar.up_indicator == "↑"
    assert scrollbar.down_indicator == "↓"
    assert scrollbar.pointer_color == colors.foreground["red"]
    assert scrollbar.indicator_color == colors.foreground["blue"]
    assert scrollbar.word_color == colors.foreground["green"]
    assert scrollbar.word_on_switch == colors.REVERSE
    assert scrollbar.background_color == colors.background["yellow"]
    assert scrollbar.background_on_switch == colors.REVERSE
    assert scrollbar.pad_right == 2
    assert scrollbar.indent == 4
    assert scrollbar.align == 2
    assert scrollbar.margin == 1
    assert scrollbar.shift == 1
    assert scrollbar.height == min(len(scrollbar.choices), 5)
    assert scrollbar.return_index is True


def test_scrollbar_empty_choices():
    with pytest.raises(ValueError, match="Choices can not be empty!"):
        ScrollBar(choices=[])


def test_scrollbar_negative_indent():
    with pytest.raises(ValueError, match="Indent must be > 0!"):
        ScrollBar(choices=["Option 1"], indent=-1)


def test_scrollbar_negative_margin():
    with pytest.raises(ValueError, match="Margin must be > 0!"):
        ScrollBar(choices=["Option 1"], margin=-1)


def test_scrollbar_move_up(mocker):
    scrollbar = ScrollBar(choices=["Option 1", "Option 2"])
    mocker.patch("bullet.utils.clearLine")
    mocker.patch("bullet.utils.moveCursorUp")
    scrollbar.pos = 1
    scrollbar.moveUp()
    assert scrollbar.pos == 0
    assert utils.clearLine.call_count == 1
    assert utils.moveCursorUp.call_count == 1


def test_scrollbar_move_down(mocker):
    scrollbar = ScrollBar(choices=["Option 1", "Option 2"])
    mocker.patch("bullet.utils.clearLine")
    mocker.patch("bullet.utils.moveCursorDown")
    scrollbar.moveDown()
    assert scrollbar.pos == 1
    assert utils.clearLine.call_count == 1
    assert utils.moveCursorDown.call_count == 1


def test_scrollbar_accept():
    scrollbar = ScrollBar(choices=["Option 1", "Option 2"], return_index=True)
    scrollbar.pos = 1
    result = scrollbar.accept()
    assert result == ("Option 2", 1)


def test_scrollbar_interrupt():
    scrollbar = ScrollBar(choices=["Option 1", "Option 2"])
    scrollbar.pos = 1
    with pytest.raises(KeyboardInterrupt):
        scrollbar.interrupt()


def test_scrollbar_launch():
    scrollbar = ScrollBar(choices=["Option 1", "Option 2"])

    # fmt: off
    with patch("bullet.utils.forceWrite") as mock_forceWrite, \
         patch("bullet.utils.moveCursorUp") as mock_moveCursorUp, \
         patch.object(ScrollBar, "handle_input", return_value="Option 1"):
    # fmt: on

        result = scrollbar.launch()

        assert result == "Option 1"
        assert mock_forceWrite.call_count == len(scrollbar.choices) * 7 # forceWrite is called 7 times per choice
        assert mock_moveCursorUp.call_count == 1
