import os
from unittest.mock import patch, MagicMock
from bullet.cursor import hide, _hide_cursor, _show_cursor


def test_hide_cursor_nt():
    """
    Test the _hide_cursor function on Windows (nt) systems.

    This test mocks the necessary ctypes.windll.kernel32 functions to simulate
    hiding the console cursor on a Windows system. It verifies that the
    GetStdHandle, GetConsoleCursorInfo, and SetConsoleCursorInfo functions are
    called with the expected arguments.

    Mocks:
        - ctypes.windll.kernel32.GetStdHandle
        - ctypes.windll.kernel32.GetConsoleCursorInfo
        - ctypes.windll.kernel32.SetConsoleCursorInfo

    Asserts:
        - GetStdHandle is called once with -11 (STD_OUTPUT_HANDLE).
        - GetConsoleCursorInfo is called once.
        - SetConsoleCursorInfo is called once.
    """
    if os.name == "nt":
        with patch("ctypes.windll.kernel32.GetStdHandle") as mock_GetStdHandle, patch(
            "ctypes.windll.kernel32.GetConsoleCursorInfo"
        ) as mock_GetConsoleCursorInfo, patch(
            "ctypes.windll.kernel32.SetConsoleCursorInfo"
        ) as mock_SetConsoleCursorInfo:
            mock_handle = MagicMock()
            mock_GetStdHandle.return_value = mock_handle
            mock_ci = MagicMock()
            mock_GetConsoleCursorInfo.return_value = mock_ci

            _hide_cursor()

            mock_GetStdHandle.assert_called_once_with(-11)
            mock_GetConsoleCursorInfo.assert_called_once()
            mock_SetConsoleCursorInfo.assert_called_once()


def test_hide_cursor_posix():
    """
    Test the _hide_cursor function on POSIX systems.

    This test checks if the _hide_cursor function correctly writes the
    escape sequence to hide the cursor ("\033[?25l") to stdout and flushes
    the output when the operating system is POSIX compliant.

    Mocks:
        sys.stdout.write: Mocked to verify the escape sequence is written.
        sys.stdout.flush: Mocked to verify the output is flushed.

    Asserts:
        - sys.stdout.write is called once with the escape sequence to hide the cursor.
        - sys.stdout.flush is called once to flush the output.
    """
    if os.name == "posix":
        with patch("sys.stdout.write") as mock_write, patch("sys.stdout.flush") as mock_flush:
            _hide_cursor()

            mock_write.assert_called_once_with("\033[?25l")
            mock_flush.assert_called_once()


def test_show_cursor_nt():
    """
    Test the _show_cursor function on Windows (nt) systems.

    This test mocks the necessary ctypes.windll.kernel32 functions to simulate
    the behavior of showing the cursor in a Windows console. It verifies that
    the correct functions are called with the expected arguments.

    Mocks:
        - ctypes.windll.kernel32.GetStdHandle
        - ctypes.windll.kernel32.GetConsoleCursorInfo
        - ctypes.windll.kernel32.SetConsoleCursorInfo

    Asserts:
        - GetStdHandle is called once with the argument -11.
        - GetConsoleCursorInfo is called once.
        - SetConsoleCursorInfo is called once.
    """
    if os.name == "nt":
        with patch("ctypes.windll.kernel32.GetStdHandle") as mock_GetStdHandle, patch(
            "ctypes.windll.kernel32.GetConsoleCursorInfo"
        ) as mock_GetConsoleCursorInfo, patch(
            "ctypes.windll.kernel32.SetConsoleCursorInfo"
        ) as mock_SetConsoleCursorInfo:
            mock_handle = MagicMock()
            mock_GetStdHandle.return_value = mock_handle
            mock_ci = MagicMock()
            mock_GetConsoleCursorInfo.return_value = mock_ci

            _show_cursor()

            mock_GetStdHandle.assert_called_once_with(-11)
            mock_GetConsoleCursorInfo.assert_called_once()
            mock_SetConsoleCursorInfo.assert_called_once()


def test_show_cursor_posix():
    """
    Test the _show_cursor function for POSIX systems.

    This test checks if the _show_cursor function correctly writes the
    escape sequence to show the cursor ("\033[?25h") to the standard output
    and flushes the output when the operating system is POSIX compliant.

    Mocks:
        sys.stdout.write: Mocked to verify the escape sequence is written.
        sys.stdout.flush: Mocked to verify the output is flushed.

    Asserts:
        mock_write.assert_called_once_with("\033[?25h"): Ensures the escape
        sequence to show the cursor is written exactly once.
        mock_flush.assert_called_once(): Ensures the output is flushed exactly once.
    """
    if os.name == "posix":
        with patch("sys.stdout.write") as mock_write, patch("sys.stdout.flush") as mock_flush:
            _show_cursor()

            mock_write.assert_called_once_with("\033[?25h")
            mock_flush.assert_called_once()


def test_hide_context_manager_nt():
    """
    Test the `hide` context manager on Windows (nt).

    This test mocks the necessary Windows API calls to verify that the `hide`
    context manager correctly interacts with the console cursor functions.

    It patches the following functions from `ctypes.windll.kernel32`:
    - GetStdHandle
    - GetConsoleCursorInfo
    - SetConsoleCursorInfo

    The test verifies that:
    - GetStdHandle is called once with the argument -11.
    - GetConsoleCursorInfo is called once.
    - SetConsoleCursorInfo is called once.
    """
    if os.name == "nt":
        with patch("ctypes.windll.kernel32.GetStdHandle") as mock_GetStdHandle, patch(
            "ctypes.windll.kernel32.GetConsoleCursorInfo"
        ) as mock_GetConsoleCursorInfo, patch(
            "ctypes.windll.kernel32.SetConsoleCursorInfo"
        ) as mock_SetConsoleCursorInfo:
            mock_handle = MagicMock()
            mock_GetStdHandle.return_value = mock_handle
            mock_ci = MagicMock()
            mock_GetConsoleCursorInfo.return_value = mock_ci

            with hide():
                mock_GetStdHandle.assert_called_once_with(-11)
                mock_GetConsoleCursorInfo.assert_called_once()
                mock_SetConsoleCursorInfo.assert_called_once()


def test_hide_context_manager_posix():
    """
    Test the hide context manager on POSIX systems.

    This test checks if the hide context manager correctly hides the cursor
    by sending the appropriate escape sequence to the standard output and
    flushing the output.

    It mocks the sys.stdout.write and sys.stdout.flush methods to verify
    that the escape sequence for hiding the cursor ("\033[?25l") is written
    to the standard output and that the output is flushed exactly once.

    The test is only executed if the operating system is POSIX compliant.
    """
    if os.name == "posix":
        with patch("sys.stdout.write") as mock_write, patch("sys.stdout.flush") as mock_flush:
            with hide():
                mock_write.assert_called_once_with("\033[?25l")
                mock_flush.assert_called_once()
