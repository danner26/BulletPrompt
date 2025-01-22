from bullet.utils import (
    is_printable,
    mygetc,
    getchar,
    moveCursorLeft,
    moveCursorRight,
    moveCursorUp,
    moveCursorDown,
    moveCursorHead,
    clearLine,
    clearConsoleUp,
    clearConsoleDown,
    forceWrite,
    cprint,
)
from bullet import colors
from bullet.charDef import UNDEFINED_KEY, ESC_KEY, ARROW_KEY_FLAG


def test_is_printable():
    """
    Tests the is_printable function to ensure it correctly identifies
    whether a string contains only printable characters.

    Test cases:
    - "Hello" should be identified as printable.
    - "Hello\n" should be identified as printable.
    - "Hello\x00" should be identified as not printable.
    """
    assert is_printable("Hello") is True
    assert is_printable("Hello\n") is True
    assert is_printable("Hello\x00") is False


def test_mygetc(mocker):
    """
    Test the `mygetc` function to ensure it reads a single character from stdin.

    This test uses the `mocker` fixture to patch several functions and methods:
    - `sys.stdin.fileno` to return a file descriptor of 0.
    - `termios.tcgetattr` to mock terminal attribute retrieval.
    - `tty.setraw` to mock setting the terminal to raw mode.
    - `sys.stdin.read` to return the character 'a'.
    - `termios.tcsetattr` to mock setting terminal attributes.

    The test asserts that:
    - The result of `mygetc()` is the character 'a'.
    - `sys.stdin.fileno` is called once.
    - `termios.tcgetattr` is called once.
    - `tty.setraw` is called once.
    - `sys.stdin.read` is called once with the argument 1.
    - `termios.tcsetattr` is called once.
    """
    mock_fd = mocker.patch("sys.stdin.fileno", return_value=0)
    mock_tcgetattr = mocker.patch("termios.tcgetattr")
    mock_setraw = mocker.patch("tty.setraw")
    mock_read = mocker.patch("sys.stdin.read", return_value="a")
    mock_tcsetattr = mocker.patch("termios.tcsetattr")

    result = mygetc()

    assert result == "a"
    mock_fd.assert_called_once()
    mock_tcgetattr.assert_called_once()
    mock_setraw.assert_called_once()
    mock_read.assert_called_once_with(1)
    mock_tcsetattr.assert_called_once()


def test_getchar(mocker):
    """
    Test the `getchar` function with various key inputs using the `mocker` library.

    This test function mocks the `bullet.utils.mygetc` function to simulate different key inputs
    and verifies that the `getchar` function returns the expected results.

    Args:
      mocker: The mocker fixture provided by the pytest-mock library.

    Test Cases:
      1. Simulate pressing the 'a' key.
      2. Simulate pressing the 'up arrow' key.
      3. Simulate pressing the 'down arrow' key.
      4. Simulate pressing the 'right arrow' key.
      5. Simulate pressing the 'left arrow' key.
      6. Simulate pressing an undefined key.

    Assertions:
      - The function asserts that the `getchar` function returns the correct character or key flag
        for each simulated key press.
    """
    mock_mygetc = mocker.patch("bullet.utils.mygetc", side_effect=["a", chr(ESC_KEY), "[", "A"])

    result = getchar()
    assert result == "a"

    mock_mygetc.side_effect = [chr(ESC_KEY), "[", "A"]
    result = getchar()
    assert result == chr(ord("A") + ARROW_KEY_FLAG)

    mock_mygetc.side_effect = [chr(ESC_KEY), "[", "B"]
    result = getchar()
    assert result == chr(ord("B") + ARROW_KEY_FLAG)

    mock_mygetc.side_effect = [chr(ESC_KEY), "[", "C"]
    result = getchar()
    assert result == chr(ord("C") + ARROW_KEY_FLAG)

    mock_mygetc.side_effect = [chr(ESC_KEY), "[", "D"]
    result = getchar()
    assert result == chr(ord("D") + ARROW_KEY_FLAG)

    mock_mygetc.side_effect = [chr(ESC_KEY), "[", "E"]
    result = getchar()
    assert result == UNDEFINED_KEY


def test_moveCursorLeft(mocker):
    """
    Test the moveCursorLeft function.

    This test verifies that the moveCursorLeft function correctly calls the
    forceWrite function with the appropriate escape sequence to move the cursor
    left by a specified number of positions.

    Args:
      mocker: A pytest-mock fixture that allows for mocking.

    Asserts:
      The forceWrite function is called once with the escape sequence "\033[5D".
    """
    mock_forceWrite = mocker.patch("bullet.utils.forceWrite")
    moveCursorLeft(5)
    mock_forceWrite.assert_called_once_with("\033[5D")


def test_moveCursorRight(mocker):
    """
    Test the moveCursorRight function.

    This test uses the mocker fixture to patch the bullet.utils.forceWrite function.
    It then calls moveCursorRight with an argument of 5 and asserts that forceWrite
    was called once with the correct escape sequence to move the cursor right by 5 positions.

    Args:
      mocker: The pytest-mock fixture used to patch functions.
    """
    mock_forceWrite = mocker.patch("bullet.utils.forceWrite")
    moveCursorRight(5)
    mock_forceWrite.assert_called_once_with("\033[5C")


def test_moveCursorUp(mocker):
    """
    Test the moveCursorUp function to ensure it correctly moves the cursor up by a specified number of lines.

    Args:
      mocker: A pytest-mock fixture that allows for mocking objects.

    Asserts:
      The forceWrite function is called once with the correct escape sequence to move the cursor up.
    """
    mock_forceWrite = mocker.patch("bullet.utils.forceWrite")
    moveCursorUp(5)
    mock_forceWrite.assert_called_once_with("\033[5A")


def test_moveCursorDown(mocker):
    """
    Test the moveCursorDown function to ensure it moves the cursor down by the specified number of lines.

    Args:
      mocker: A pytest-mock fixture that allows for mocking objects in the test.

    Asserts:
      The forceWrite function is called once with the correct escape sequence to move the cursor down.
    """
    mock_forceWrite = mocker.patch("bullet.utils.forceWrite")
    moveCursorDown(5)
    mock_forceWrite.assert_called_once_with("\033[5B")


def test_moveCursorHead(mocker):
    """
    Test the moveCursorHead function.

    This test uses the mocker fixture to patch the forceWrite function from the bullet.utils module.
    It then calls the moveCursorHead function and asserts that forceWrite was called exactly once with the argument "\r".

    Args:
      mocker: The pytest-mock fixture used to mock objects during testing.
    """
    mock_forceWrite = mocker.patch("bullet.utils.forceWrite")
    moveCursorHead()
    mock_forceWrite.assert_called_once_with("\r")


def test_clearLine(mocker):
    """
    Test the clearLine function.

    This test uses the mocker fixture to patch the 'forceWrite' and 'moveCursorHead'
    functions from the 'bullet.utils' module. It verifies that the 'clearLine'
    function calls 'forceWrite' with a string of 80 spaces and 'moveCursorHead' once.

    Args:
      mocker: A fixture used to mock objects for testing.
    """
    mock_forceWrite = mocker.patch("bullet.utils.forceWrite")
    mock_moveCursorHead = mocker.patch("bullet.utils.moveCursorHead")
    clearLine()
    mock_forceWrite.assert_called_once_with(" " * 80)
    mock_moveCursorHead.assert_called_once()


def test_clearConsoleUp(mocker):
    """
    Test the clearConsoleUp function to ensure it calls the clearLine and moveCursorUp
    functions the correct number of times.

    Args:
      mocker: A pytest-mock fixture that allows for mocking objects in the test.

    Patches:
      bullet.utils.clearLine: Mocked to track the number of times it is called.
      bullet.utils.moveCursorUp: Mocked to track the number of times it is called.

    Asserts:
      The clearLine function is called 3 times.
      The moveCursorUp function is called 3 times.
    """
    mock_clearLine = mocker.patch("bullet.utils.clearLine")
    mock_moveCursorUp = mocker.patch("bullet.utils.moveCursorUp")
    clearConsoleUp(3)
    assert mock_clearLine.call_count == 3
    assert mock_moveCursorUp.call_count == 3


def test_clearConsoleDown(mocker):
    """
    Test the clearConsoleDown function.

    This test verifies that the clearConsoleDown function correctly calls the
    clearLine, moveCursorDown, and moveCursorUp functions the expected number
    of times.

    Args:
      mocker: A pytest-mock fixture that allows for mocking objects.

    Asserts:
      - clearLine is called 3 times.
      - moveCursorDown is called 3 times.
      - moveCursorUp is called once with the argument 3.
    """
    mock_clearLine = mocker.patch("bullet.utils.clearLine")
    mock_moveCursorDown = mocker.patch("bullet.utils.moveCursorDown")
    mock_moveCursorUp = mocker.patch("bullet.utils.moveCursorUp")
    clearConsoleDown(3)
    assert mock_clearLine.call_count == 3
    assert mock_moveCursorDown.call_count == 3
    mock_moveCursorUp.assert_called_once_with(3)


def test_forceWrite(mocker):
    """
    Test the forceWrite function.

    This test uses the mocker fixture to patch the sys.stdout.write and
    sys.stdout.flush methods. It verifies that the forceWrite function
    writes the expected string to stdout and flushes the output.

    Args:
      mocker: A pytest fixture used to mock objects for testing.
    """
    mock_stdout_write = mocker.patch("sys.stdout.write")
    mock_stdout_flush = mocker.patch("sys.stdout.flush")
    forceWrite("Hello")
    mock_stdout_write.assert_called_once_with("Hello")
    mock_stdout_flush.assert_called_once()


def test_cprint(mocker):
    """
    Test the cprint function to ensure it correctly formats and prints colored text.

    Args:
      mocker: A pytest-mock fixture used to patch the forceWrite function.

    Asserts:
      The forceWrite function is called once with the expected formatted string and end character.
    """
    mock_forceWrite = mocker.patch("bullet.utils.forceWrite")
    cprint("Hello", color=colors.foreground["red"], on=colors.background["blue"], end="!")
    mock_forceWrite.assert_called_once_with(
        colors.background["blue"] + colors.foreground["red"] + "Hello" + colors.RESET, end="!"
    )
