import pytest
from unittest.mock import patch
from bullet.client import Check
from bullet import colors, utils


def test_check_initialization():
    """
    Test the initialization of the Check class.

    This test verifies that the Check object is initialized with the correct
    attributes and values. It checks the following properties:
    - prompt: The prompt message to display.
    - choices: The list of choices available.
    - check: The symbol used for the check mark.
    - check_color: The color of the check mark.
    - check_on_switch: The color of the check mark when selected.
    - word_color: The color of the choice text.
    - word_on_switch: The color of the choice text when selected.
    - background_color: The background color of the choice.
    - background_on_switch: The background color of the choice when selected.
    - pad_right: The padding to the right of the choice text.
    - indent: The indentation level of the choices.
    - align: The alignment of the choices.
    - margin: The margin around the choices.
    - shift: The shift value for the choices.
    - return_index: Whether to return the index of the selected choice.

    Assertions:
    - The prompt is correctly set.
    - The choices are correctly set.
    - The check symbol is correctly set.
    - The check color is correctly set.
    - The check color on switch is correctly set.
    - The word color is correctly set.
    - The word color on switch is correctly set.
    - The background color is correctly set.
    - The background color on switch is correctly set.
    - The padding to the right is correctly set.
    - The indentation level is correctly set.
    - The alignment is correctly set.
    - The margin is correctly set.
    - The shift value is correctly set.
    - The return_index flag is correctly set to True.
    """
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
    """
    Test that Check raises a ValueError when initialized with empty choices.

    This test ensures that the Check class correctly raises a ValueError
    with the message "Choices can not be empty!" when it is initialized
    with an empty list of choices.
    """
    with pytest.raises(ValueError, match="Choices can not be empty!"):
        Check(choices=[])


def test_check_negative_indent():
    """
    Test that Check raises a ValueError when a negative indent is provided.

    This test ensures that the Check class correctly handles invalid input
    by raising a ValueError when the indent parameter is less than or equal to zero.

    Raises:
        ValueError: If the indent parameter is less than or equal to zero.
    """
    with pytest.raises(ValueError, match="Indent must be > 0!"):
        Check(choices=["Option 1"], indent=-1)


def test_check_negative_margin():
    """
    Test that Check raises a ValueError when a negative margin is provided.

    This test ensures that the Check class correctly raises a ValueError
    with the message "Margin must be > 0!" when initialized with a negative
    margin value.

    Raises:
        ValueError: If the margin is less than or equal to 0.
    """
    with pytest.raises(ValueError, match="Margin must be > 0!"):
        Check(choices=["Option 1"], margin=-1)


def test_check_render_rows(mocker):
    """
    Test the renderRows method of the Check class.

    This test verifies that the renderRows method of the Check class correctly
    calls the forceWrite function the expected number of times. The Check class
    is initialized with two choices, and the forceWrite function is expected to
    be called twice per choice (once for the row and once for the newline).

    Args:
        mocker: A pytest-mock fixture used to patch the forceWrite function.

    Asserts:
        The forceWrite function is called 12 times (2 choices * 2 calls per choice * 3 rows).
    """
    check = Check(choices=["Option 1", "Option 2"])
    mocker.patch("bullet.utils.forceWrite")
    check.renderRows()
    assert utils.forceWrite.call_count == len(check.choices) * 6  # forceWrite is called 6 times per choice


def test_check_print_row(mocker):
    """
    Test the `printRow` method of the `Check` class.

    This test verifies that the `printRow` method correctly calls the necessary
    utility functions to print a row. It uses the `mocker` fixture to patch the
    `forceWrite`, `cprint`, and `moveCursorHead` functions from the `bullet.utils`
    module and checks that they are called the expected number of times.

    Args:
        mocker: The mocker fixture used to patch functions.
    """
    check = Check(choices=["Option 1", "Option 2"])
    mocker.patch("bullet.utils.forceWrite")
    mocker.patch("bullet.utils.cprint")
    mocker.patch("bullet.utils.moveCursorHead")
    check.printRow(0)
    assert utils.forceWrite.call_count == 1
    assert utils.cprint.call_count == 3
    assert utils.moveCursorHead.call_count == 1


def test_check_move_up(mocker):
    """
    Test the `moveUp` method of the `Check` class.

    This test verifies that the `moveUp` method correctly updates the position
    and calls the necessary utility functions to clear the line and move the cursor up.

    Args:
        mocker: A fixture provided by the pytest-mock plugin to mock objects.

    Steps:
    1. Create an instance of the `Check` class with two choices.
    2. Mock the `clearLine` and `moveCursorUp` functions from the `bullet.utils` module.
    3. Set the initial position (`pos`) of the `Check` instance to 1.
    4. Call the `moveUp` method.
    5. Assert that the position (`pos`) is updated to 0.
    6. Assert that the `clearLine` function is called once.
    7. Assert that the `moveCursorUp` function is called once.
    """
    check = Check(choices=["Option 1", "Option 2"])
    mocker.patch("bullet.utils.clearLine")
    mocker.patch("bullet.utils.moveCursorUp")
    check.pos = 1
    check.moveUp()
    assert check.pos == 0
    assert utils.clearLine.call_count == 1
    assert utils.moveCursorUp.call_count == 1


def test_check_move_down(mocker):
    """
    Test the `moveDown` method of the `Check` class.

    This test verifies that when the `moveDown` method is called:
    - The position (`pos`) of the `Check` instance is updated correctly.
    - The `clearLine` utility function is called once.
    - The `moveCursorDown` utility function is called once.

    Args:
        mocker: A fixture for mocking objects and functions.
    """
    check = Check(choices=["Option 1", "Option 2"])
    mocker.patch("bullet.utils.clearLine")
    mocker.patch("bullet.utils.moveCursorDown")
    check.moveDown()
    assert check.pos == 1
    assert utils.clearLine.call_count == 1
    assert utils.moveCursorDown.call_count == 1


def test_check_toggle_row(mocker):
    """
    Test the toggleRow method of the Check class.

    This test verifies that the toggleRow method correctly toggles the state
    of the first row in the Check instance's choices. It uses the mocker
    fixture to patch the clearLine function from the bullet.utils module.

    Args:
        mocker: A fixture for mocking objects during testing.

    Asserts:
        - The first row is checked (True) after the first toggleRow call.
        - The first row is unchecked (False) after the second toggleRow call.
    """
    check = Check(choices=["Option 1", "Option 2"])
    mocker.patch("bullet.utils.clearLine")
    check.toggleRow()
    assert check.checked[0] is True
    check.toggleRow()
    assert check.checked[0] is False


def test_check_accept():
    """
    Test the accept method of the Check class.

    This test verifies that the accept method correctly returns the selected choices
    and their corresponding indices when the return_index parameter is set to True.

    Steps:
    1. Create an instance of the Check class with two choices and return_index set to True.
    2. Set the checked attribute to indicate that the first choice is selected.
    3. Call the accept method.
    4. Assert that the result is a tuple containing a list with the selected choice and a list with the index of the selected choice.

    Expected Result:
    The accept method should return (["Option 1"], [0]).
    """
    check = Check(choices=["Option 1", "Option 2"], return_index=True)
    check.checked = [True, False]
    result = check.accept()
    assert result == (["Option 1"], [0])


def test_check_interrupt():
    """
    Test the interrupt method of the Check class.

    This test sets up a Check instance with two choices and sets its position to 1.
    It then verifies that calling the interrupt method raises a KeyboardInterrupt exception.

    Raises:
        KeyboardInterrupt: When the interrupt method is called.
    """
    check = Check(choices=["Option 1", "Option 2"])
    check.pos = 1
    with pytest.raises(KeyboardInterrupt):
        check.interrupt()


def test_check_launch(mocker):
    """
    Test the `launch` method of the `Check` class.

    This test uses the `mocker` fixture to patch the `forceWrite` and `moveCursorUp`
    functions from the `bullet.utils` module, as well as the `handle_input` method
    of the `Check` class. It verifies that the `launch` method returns the expected
    result and that the patched functions are called the expected number of times.

    Args:
        mocker (pytest_mock.plugin.MockerFixture): The mocker fixture provided by pytest-mock.

    Asserts:
        The result of the `launch` method is `["Option 1"]`.
        The `forceWrite` function is called 12 times.
        The `moveCursorUp` function is called once.
    """
    check = Check(choices=["Option 1", "Option 2"])

    # fmt: off
    with patch("bullet.utils.forceWrite") as mock_forceWrite, \
         patch("bullet.utils.moveCursorUp") as mock_moveCursorUp, \
         patch("bullet.client.Check.handle_input", return_value=["Option 1"]):
         # fmt: on

        result = check.launch()

        assert result == ["Option 1"]
        assert mock_forceWrite.call_count == len(check.choices) * 6 # forceWrite is called 6 times per choice
        assert mock_moveCursorUp.call_count == 1
