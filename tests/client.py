import pytest
from unittest.mock import patch
from bullet.client import Bullet
from bullet import colors, utils


def test_bullet_initialization():
    bullet = Bullet(
        prompt="Select an option:",
        choices=["Option 1", "Option 2"],
        bullet="*",
        bullet_color=colors.foreground["red"],
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
    assert bullet.prompt == "Select an option:"
    assert bullet.choices == ["Option 1", "Option 2"]
    assert bullet.bullet == "*"
    assert bullet.bullet_color == colors.foreground["red"]
    assert bullet.word_color == colors.foreground["blue"]
    assert bullet.word_on_switch == colors.REVERSE
    assert bullet.background_color == colors.background["yellow"]
    assert bullet.background_on_switch == colors.REVERSE
    assert bullet.pad_right == 2
    assert bullet.indent == 4
    assert bullet.align == 2
    assert bullet.margin == 1
    assert bullet.shift == 1
    assert bullet.return_index is True


def test_bullet_empty_choices():
    with pytest.raises(ValueError, match="Choices can not be empty!"):
        Bullet(choices=[])


def test_bullet_negative_indent():
    with pytest.raises(ValueError, match="Indent must be > 0!"):
        Bullet(choices=["Option 1"], indent=-1)


def test_bullet_negative_margin():
    with pytest.raises(ValueError, match="Margin must be > 0!"):
        Bullet(choices=["Option 1"], margin=-1)


def test_bullet_render_bullets(mocker):
    bullet = Bullet(choices=["Option 1", "Option 2"])
    mocker.patch("bullet.utils.forceWrite")
    bullet.renderBullets()
    assert utils.forceWrite.call_count == 12  # 2 choices * 2 calls per choice (bullet + newline)


def test_bullet_print_bullet(mocker):
    bullet = Bullet(choices=["Option 1", "Option 2"])
    mocker.patch("bullet.utils.forceWrite")
    mocker.patch("bullet.utils.cprint")
    mocker.patch("bullet.utils.moveCursorHead")
    bullet.printBullet(0)
    assert utils.forceWrite.call_count == 1
    assert utils.cprint.call_count == 3
    assert utils.moveCursorHead.call_count == 1


def test_bullet_move_up(mocker):
    bullet = Bullet(choices=["Option 1", "Option 2"])
    mocker.patch("bullet.utils.clearLine")
    mocker.patch("bullet.utils.moveCursorUp")
    bullet.pos = 1
    bullet.moveUp()
    assert bullet.pos == 0
    assert utils.clearLine.call_count == 1
    assert utils.moveCursorUp.call_count == 1


def test_bullet_move_down(mocker):
    bullet = Bullet(choices=["Option 1", "Option 2"])
    mocker.patch("bullet.utils.clearLine")
    mocker.patch("bullet.utils.moveCursorDown")
    bullet.moveDown()
    assert bullet.pos == 1
    assert utils.clearLine.call_count == 1
    assert utils.moveCursorDown.call_count == 1


def test_bullet_accept():
    bullet = Bullet(choices=["Option 1", "Option 2"], return_index=True)
    bullet.pos = 1
    result = bullet.accept()
    assert result == ("Option 2", 1)


def test_bullet_interrupt():
    bullet = Bullet(choices=["Option 1", "Option 2"])
    bullet.pos = 1
    with pytest.raises(KeyboardInterrupt):
        bullet.interrupt()


def test_bullet_launch():
    bullet = Bullet(choices=["Option 1", "Option 2"])

    with patch("bullet.utils.forceWrite") as mock_forceWrite, patch(
        "bullet.utils.moveCursorUp"
    ) as mock_moveCursorUp, patch("bullet.client.Bullet.handle_input", return_value="Option 1"):
        result = bullet.launch()

        assert result == "Option 1"
        assert mock_forceWrite.call_count == 12
        assert mock_moveCursorUp.call_count == 1
