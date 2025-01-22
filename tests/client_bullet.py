import pytest
from unittest.mock import patch
from bullet.client import Bullet
from bullet import colors, utils


def test_bullet_initialization():
    """
    Test the initialization of the Bullet class.

    This test verifies that the Bullet object is initialized with the correct
    attributes based on the provided parameters.

    Assertions:
        - The prompt is set to "Select an option:".
        - The choices are set to ["Option 1", "Option 2"].
        - The bullet character is set to "*".
        - The bullet color is set to red.
        - The word color is set to blue.
        - The word on switch color is set to REVERSE.
        - The background color is set to yellow.
        - The background on switch color is set to REVERSE.
        - The pad right value is set to 2.
        - The indent value is set to 4.
        - The align value is set to 2.
        - The margin value is set to 1.
        - The shift value is set to 1.
        - The return_index flag is set to True.
    """
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
    """
    Test that Bullet raises a ValueError when initialized with empty choices.

    This test ensures that the Bullet class correctly handles the case where
    an empty list is provided for the choices parameter. It expects a ValueError
    to be raised with the message "Choices can not be empty!".
    """
    with pytest.raises(ValueError, match="Choices can not be empty!"):
        Bullet(choices=[])


def test_bullet_negative_indent():
    """
    Test that Bullet raises a ValueError when initialized with a negative indent.

    This test ensures that the Bullet class correctly handles invalid input for the
    indent parameter by raising a ValueError with the appropriate error message.

    Raises:
        ValueError: If the indent parameter is less than or equal to 0.
    """
    with pytest.raises(ValueError, match="Indent must be > 0!"):
        Bullet(choices=["Option 1"], indent=-1)


def test_bullet_negative_margin():
    """
    Test that creating a Bullet instance with a negative margin raises a ValueError.

    This test verifies that the Bullet class correctly handles invalid input for the
    margin parameter by raising a ValueError when the margin is less than or equal to zero.

    Raises:
        ValueError: If the margin is less than or equal to zero, with the message "Margin must be > 0!".
    """
    with pytest.raises(ValueError, match="Margin must be > 0!"):
        Bullet(choices=["Option 1"], margin=-1)


def test_bullet_render_bullets(mocker):
    """
    Test the `renderBullets` method of the `Bullet` class.

    This test verifies that the `renderBullets` method calls the `forceWrite`
    function from the `bullet.utils` module the expected number of times.

    Args:
        mocker: A fixture provided by the pytest-mock plugin to mock objects.

    Setup:
        - Creates an instance of the `Bullet` class with two choices.
        - Mocks the `forceWrite` function from the `bullet.utils` module.

    Test:
        - Calls the `renderBullets` method on the `Bullet` instance.
        - Asserts that the `forceWrite` function is called 12 times.
    """
    bullet = Bullet(choices=["Option 1", "Option 2"])
    mocker.patch("bullet.utils.forceWrite")
    bullet.renderBullets()
    assert utils.forceWrite.call_count == len(bullet.choices) * 6  # forceWrite is called 6 times per choice


def test_bullet_print_bullet(mocker):
    """
    Test the `printBullet` method of the `Bullet` class.

    This test verifies that the `printBullet` method correctly calls the
    `forceWrite`, `cprint`, and `moveCursorHead` utility functions the
    expected number of times.

    Args:
        mocker: A fixture provided by the pytest-mock plugin to mock objects.

    Asserts:
        - `utils.forceWrite` is called exactly once.
        - `utils.cprint` is called exactly three times.
        - `utils.moveCursorHead` is called exactly once.
    """
    bullet = Bullet(choices=["Option 1", "Option 2"])
    mocker.patch("bullet.utils.forceWrite")
    mocker.patch("bullet.utils.cprint")
    mocker.patch("bullet.utils.moveCursorHead")
    bullet.printBullet(0)
    assert utils.forceWrite.call_count == 1
    assert utils.cprint.call_count == 3
    assert utils.moveCursorHead.call_count == 1


def test_bullet_move_up(mocker):
    """
    Test the `moveUp` method of the `Bullet` class.

    This test verifies that the `moveUp` method correctly updates the position
    of the bullet and calls the necessary utility functions to clear the line
    and move the cursor up.

    Args:
        mocker: A fixture for mocking objects.

    Steps:
    1. Create a `Bullet` instance with two choices.
    2. Mock the `clearLine` and `moveCursorUp` functions from the `bullet.utils` module.
    3. Set the initial position of the bullet to 1.
    4. Call the `moveUp` method.
    5. Assert that the position of the bullet is updated to 0.
    6. Assert that the `clearLine` function is called once.
    7. Assert that the `moveCursorUp` function is called once.
    """
    bullet = Bullet(choices=["Option 1", "Option 2"])
    mocker.patch("bullet.utils.clearLine")
    mocker.patch("bullet.utils.moveCursorUp")
    bullet.pos = 1
    bullet.moveUp()
    assert bullet.pos == 0
    assert utils.clearLine.call_count == 1
    assert utils.moveCursorUp.call_count == 1


def test_bullet_move_down(mocker):
    """
    Test the `moveDown` method of the `Bullet` class.

    This test verifies that when the `moveDown` method is called:
    1. The `pos` attribute of the `Bullet` instance is incremented by 1.
    2. The `clearLine` utility function is called exactly once.
    3. The `moveCursorDown` utility function is called exactly once.

    Args:
        mocker (MockerFixture): The mocker fixture provided by pytest-mock for patching.

    Asserts:
        bullet.pos == 1: Ensures the position is updated correctly.
        utils.clearLine.call_count == 1: Ensures `clearLine` is called once.
        utils.moveCursorDown.call_count == 1: Ensures `moveCursorDown` is called once.
    """
    bullet = Bullet(choices=["Option 1", "Option 2"])
    mocker.patch("bullet.utils.clearLine")
    mocker.patch("bullet.utils.moveCursorDown")
    bullet.moveDown()
    assert bullet.pos == 1
    assert utils.clearLine.call_count == 1
    assert utils.moveCursorDown.call_count == 1


def test_bullet_accept():
    """
    Test the accept method of the Bullet class.

    This test verifies that the accept method correctly returns the selected
    choice and its index when the bullet position is set to a specific value.

    Steps:
    1. Create a Bullet instance with a list of choices and set return_index to True.
    2. Set the bullet position to 1 (second choice).
    3. Call the accept method and store the result.
    4. Assert that the result is a tuple containing the selected choice and its index.

    Expected Result:
    The result should be ("Option 2", 1).
    """
    bullet = Bullet(choices=["Option 1", "Option 2"], return_index=True)
    bullet.pos = 1
    result = bullet.accept()
    assert result == ("Option 2", 1)


def test_bullet_interrupt():
    """
    Test the interrupt method of the Bullet class.

    This test initializes a Bullet instance with two choices and sets its position
    to 1. It then verifies that calling the interrupt method raises a KeyboardInterrupt
    exception.

    Raises:
        KeyboardInterrupt: When the interrupt method is called.
    """
    bullet = Bullet(choices=["Option 1", "Option 2"])
    bullet.pos = 1
    with pytest.raises(KeyboardInterrupt):
        bullet.interrupt()


def test_bullet_launch():
    """
    Test the `launch` method of the `Bullet` class.

    This test verifies that the `launch` method correctly handles user input and
    returns the expected result. It also checks that the `forceWrite` and
    `moveCursorUp` utility functions are called the expected number of times.

    Steps:
    1. Create a `Bullet` instance with two choices: "Option 1" and "Option 2".
    2. Patch the `forceWrite` and `moveCursorUp` utility functions.
    3. Patch the `handle_input` method of the `Bullet` class to return "Option 1".
    4. Call the `launch` method of the `Bullet` instance.
    5. Assert that the result of the `launch` method is "Option 1".
    6. Assert that `forceWrite` is called 12 times.
    7. Assert that `moveCursorUp` is called once.
    """
    bullet = Bullet(choices=["Option 1", "Option 2"])

    # fmt: off
    with patch("bullet.utils.forceWrite") as mock_forceWrite, \
         patch("bullet.utils.moveCursorUp") as mock_moveCursorUp, \
         patch("bullet.client.Bullet.handle_input", return_value="Option 1"):
         # fmt: on

        result = bullet.launch()

        assert result == "Option 1"
        assert mock_forceWrite.call_count == len(bullet.choices) * 6 # forceWrite is called 6 times per choice
        assert mock_moveCursorUp.call_count == 1
