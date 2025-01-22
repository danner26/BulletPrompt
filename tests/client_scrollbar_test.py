import pytest
from bullet.client import ScrollBar
from bullet import colors, utils
from unittest.mock import patch


def test_scrollbar_initialization():
    """
    Test the initialization of the ScrollBar class.

    This test verifies that the ScrollBar object is initialized with the correct
    attributes based on the provided parameters.

    Assertions:
        - The prompt is correctly set.
        - The choices are correctly set.
        - The pointer is correctly set.
        - The up_indicator is correctly set.
        - The down_indicator is correctly set.
        - The pointer_color is correctly set.
        - The indicator_color is correctly set.
        - The word_color is correctly set.
        - The word_on_switch is correctly set.
        - The background_color is correctly set.
        - The background_on_switch is correctly set.
        - The pad_right is correctly set.
        - The indent is correctly set.
        - The align is correctly set.
        - The margin is correctly set.
        - The shift is correctly set.
        - The height is set to the minimum of the number of choices and the provided height.
        - The return_index is correctly set to True.
    """
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
    """
    Test that creating a ScrollBar with empty choices raises a ValueError.

    This test ensures that when an attempt is made to create a ScrollBar
    object with an empty list of choices, a ValueError is raised with the
    appropriate error message "Choices can not be empty!".

    Raises:
        ValueError: If the choices list is empty.
    """
    with pytest.raises(ValueError, match="Choices can not be empty!"):
        ScrollBar(choices=[])


def test_scrollbar_negative_indent():
    """
    Test that creating a ScrollBar with a negative indent raises a ValueError.

    This test verifies that the ScrollBar class correctly raises a ValueError
    when initialized with a negative indent value. The error message should
    match "Indent must be > 0!".

    Raises:
        ValueError: If the indent value is negative.
    """
    with pytest.raises(ValueError, match="Indent must be > 0!"):
        ScrollBar(choices=["Option 1"], indent=-1)


def test_scrollbar_negative_margin():
    """
    Test that the ScrollBar raises a ValueError when initialized with a negative margin.

    This test ensures that the ScrollBar class correctly handles invalid input
    by raising a ValueError when the margin is set to a negative value.

    Raises:
        ValueError: If the margin is less than or equal to 0.
    """
    with pytest.raises(ValueError, match="Margin must be > 0!"):
        ScrollBar(choices=["Option 1"], margin=-1)


def test_scrollbar_move_up(mocker):
    """
    Test the `moveUp` method of the `ScrollBar` class.

    This test verifies that when the `moveUp` method is called:
    1. The scrollbar position (`pos`) is decremented by 1.
    2. The `clearLine` utility function is called once.
    3. The `moveCursorUp` utility function is called once.

    Args:
        mocker: A pytest fixture used to mock functions.

    Setup:
        - A `ScrollBar` instance is created with two choices.
        - The `clearLine` and `moveCursorUp` functions from the `bullet.utils` module are mocked.
        - The initial position of the scrollbar is set to 1.

    Assertions:
        - After calling `moveUp`, the scrollbar position should be 0.
        - The `clearLine` function should be called once.
        - The `moveCursorUp` function should be called once.
    """
    scrollbar = ScrollBar(choices=["Option 1", "Option 2"])
    mocker.patch("bullet.utils.clearLine")
    mocker.patch("bullet.utils.moveCursorUp")
    scrollbar.pos = 1
    scrollbar.moveUp()
    assert scrollbar.pos == 0
    assert utils.clearLine.call_count == 1
    assert utils.moveCursorUp.call_count == 1


def test_scrollbar_move_down(mocker):
    """
    Test the `moveDown` method of the `ScrollBar` class.

    This test verifies that the scrollbar moves down correctly when the `moveDown` method is called.
    It mocks the `clearLine` and `moveCursorDown` functions from the `bullet.utils` module to ensure
    they are called the correct number of times during the operation.

    Args:
        mocker: A pytest fixture used to mock objects.

    Asserts:
        - The scrollbar's position (`pos`) is updated to 1 after moving down.
        - The `clearLine` function is called exactly once.
        - The `moveCursorDown` function is called exactly once.
    """
    scrollbar = ScrollBar(choices=["Option 1", "Option 2"])
    mocker.patch("bullet.utils.clearLine")
    mocker.patch("bullet.utils.moveCursorDown")
    scrollbar.moveDown()
    assert scrollbar.pos == 1
    assert utils.clearLine.call_count == 1
    assert utils.moveCursorDown.call_count == 1


def test_scrollbar_accept():
    """
    Test the accept method of the ScrollBar class.

    This test creates a ScrollBar instance with two options and sets the position
    to the second option. It then calls the accept method and asserts that the
    returned value is a tuple containing the selected option and its index.

    Assertions:
        - The result of the accept method should be ("Option 2", 1).
    """
    scrollbar = ScrollBar(choices=["Option 1", "Option 2"], return_index=True)
    scrollbar.pos = 1
    result = scrollbar.accept()
    assert result == ("Option 2", 1)


def test_scrollbar_interrupt():
    """
    Test the interrupt functionality of the ScrollBar class.

    This test initializes a ScrollBar instance with two choices and sets its position to 1.
    It then simulates an interrupt by calling the `interrupt` method and expects a
    KeyboardInterrupt to be raised.

    Raises:
        KeyboardInterrupt: If the interrupt method is called.
    """
    scrollbar = ScrollBar(choices=["Option 1", "Option 2"])
    scrollbar.pos = 1
    with pytest.raises(KeyboardInterrupt):
        scrollbar.interrupt()


def test_scrollbar_launch():
    """
    Test the launch method of the ScrollBar class.

    This test verifies that the ScrollBar's launch method correctly handles user input
    and interacts with the necessary utility functions.

    Steps:
    1. Create a ScrollBar instance with a list of choices.
    2. Patch the `bullet.utils.forceWrite` and `bullet.utils.moveCursorUp` functions.
    3. Patch the `handle_input` method of the ScrollBar instance to return a specific choice.
    4. Call the `launch` method of the ScrollBar instance.
    5. Assert that the result of the `launch` method is the expected choice.
    6. Assert that `forceWrite` is called the expected number of times.
    7. Assert that `moveCursorUp` is called once.

    Assertions:
    - The result of the `launch` method should be "Option 1".
    - The `forceWrite` function should be called 7 times per choice.
    - The `moveCursorUp` function should be called once.
    """
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
