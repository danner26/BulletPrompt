import pytest
from unittest.mock import patch
from bullet.client import Check
from bullet import colors, utils


def test_check_initialization():
    check = Check(
        prompt="Select options:",
        choices=["Option 1", "Option 2"],
        check="√",
        check_color=colors.foreground["red"],
        check_on_switch=colors.REVERSE,
        word_color=colors.foreground["blue"],
        word_on_switch=colors.REVERSE,
        background_color=colors.background["yellow"],
        background_on_switch=colors.REVERSE,
        pad_right=2,
        indent=4,
        align=2,
        margin=1,
        shift=1,
        return_index=True,
    )
    assert check.prompt == "Select options:"
    assert check.choices == ["Option 1", "Option 2"]
    assert check.check == "√"
    assert check.check_color == colors.foreground["red"]
    assert check.check_on_switch == colors.REVERSE
    assert check.word_color == colors.foreground["blue"]
    assert check.word_on_switch == colors.REVERSE
    assert check.background_color == colors.background["yellow"]
    assert check.background_on_switch == colors.REVERSE
    assert check.pad_right == 2
    assert check.indent == 4
    assert check.align == 2
    assert check.margin == 1
    assert check.shift == 1
    assert check.return_index is True


def test_check_empty_choices():
    with pytest.raises(ValueError, match="Choices can not be empty!"):
        Check(choices=[])


def test_check_negative_indent():
    with pytest.raises(ValueError, match="Indent must be > 0!"):
        Check(choices=["Option 1"], indent=-1)


def test_check_negative_margin():
    with pytest.raises(ValueError, match="Margin must be > 0!"):
        Check(choices=["Option 1"], margin=-1)


def test_check_render_rows(mocker):
    check = Check(choices=["Option 1", "Option 2"])
    mocker.patch("bullet.utils.forceWrite")
    check.renderRows()
    assert utils.forceWrite.call_count == 12  # 2 choices * 2 calls per choice (row + newline)


def test_check_print_row(mocker):
    check = Check(choices=["Option 1", "Option 2"])
    mocker.patch("bullet.utils.forceWrite")
    mocker.patch("bullet.utils.cprint")
    mocker.patch("bullet.utils.moveCursorHead")
    check.printRow(0)
    assert utils.forceWrite.call_count == 1
    assert utils.cprint.call_count == 3
    assert utils.moveCursorHead.call_count == 1


def test_check_move_up(mocker):
    check = Check(choices=["Option 1", "Option 2"])
    mocker.patch("bullet.utils.clearLine")
    mocker.patch("bullet.utils.moveCursorUp")
    check.pos = 1
    check.moveUp()
    assert check.pos == 0
    assert utils.clearLine.call_count == 1
    assert utils.moveCursorUp.call_count == 1


def test_check_move_down(mocker):
    check = Check(choices=["Option 1", "Option 2"])
    mocker.patch("bullet.utils.clearLine")
    mocker.patch("bullet.utils.moveCursorDown")
    check.moveDown()
    assert check.pos == 1
    assert utils.clearLine.call_count == 1
    assert utils.moveCursorDown.call_count == 1


def test_check_toggle_row(mocker):
    check = Check(choices=["Option 1", "Option 2"])
    mocker.patch("bullet.utils.clearLine")
    check.toggleRow()
    assert check.checked[0] is True
    check.toggleRow()
    assert check.checked[0] is False


def test_check_accept():
    check = Check(choices=["Option 1", "Option 2"], return_index=True)
    check.checked = [True, False]
    result = check.accept()
    assert result == (["Option 1"], [0])


def test_check_interrupt():
    check = Check(choices=["Option 1", "Option 2"])
    check.pos = 1
    with pytest.raises(KeyboardInterrupt):
        check.interrupt()


def test_check_launch(mocker):
    check = Check(choices=["Option 1", "Option 2"])

    # fmt: off
    with patch("bullet.utils.forceWrite") as mock_forceWrite, \
         patch("bullet.utils.moveCursorUp") as mock_moveCursorUp, \
         patch("bullet.client.Check.handle_input", return_value=["Option 1"]):
    # fmt: on

        result = check.launch()

        assert result == ["Option 1"]
        assert mock_forceWrite.call_count == 12
        assert mock_moveCursorUp.call_count == 1
