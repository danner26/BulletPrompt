import pytest
from bullet.client import YesNo
from bullet import colors
from unittest.mock import patch


def test_yesno_initialization():
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
    with pytest.raises(ValueError, match="Prompt can not be empty!"):
        YesNo(prompt="")


def test_yesno_invalid_default():
    with pytest.raises(ValueError, match="`default` can only be 'y' or 'n'!"):
        YesNo(prompt="Do you want to continue?", default="maybe")


def test_yesno_valid():
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
    yesno = YesNo(prompt="Do you want to continue?")

    with patch("bullet.utils.forceWrite") as mock_forceWrite, patch.object(
        yesno, "valid", side_effect=[False, True]
    ), patch("bullet.client.myInput.input", return_value="y"):
        result = yesno.launch()

        assert result
        assert mock_forceWrite.call_count > 0
