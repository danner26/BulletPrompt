from unittest.mock import patch
from bullet.keyhandler import register, init
from bullet.charDef import UNDEFINED_KEY


def test_register_decorator():
    """
    Tests the `register` decorator to ensure that it correctly assigns the `_handle_key` attribute
    to the decorated functions.

    The test performs the following checks:
    1. Decorates `handle_a` with `register(65)` and verifies that the `_handle_key` attribute is set to `[65]`.
    2. Decorates `handle_b` with `register(66)` and verifies that the `_handle_key` attribute is set to `[66]`.
    3. Decorates `handle_c` with `register(67)` and verifies that the `_handle_key` attribute is set to `[67]`.

    Assertions:
    - Each decorated function should have the `_handle_key` attribute.
    - The `_handle_key` attribute should contain the correct ASCII value.
    """

    @register(65)  # ASCII for 'A'
    def handle_a():
        return "Handled A"

    assert hasattr(handle_a, "_handle_key")
    assert handle_a._handle_key == [65]

    @register(66)  # ASCII for 'B'
    def handle_b():
        return "Handled B"

    assert hasattr(handle_b, "_handle_key")
    assert handle_b._handle_key == [66]

    @register(67)  # ASCII for 'C'
    def handle_c():
        return "Handled C"

    assert hasattr(handle_c, "_handle_key")
    assert handle_c._handle_key == [67]


def test_init_decorator():
    """
    Test the `init` decorator and `register` decorator functionality.

    This test verifies that:
    1. The `init` decorator properly initializes the class with a `_key_handler` attribute.
    2. The `register` decorator correctly registers methods to specific ASCII key codes.
    3. The `_key_handler` attribute contains the correct mappings for the registered key codes.

    Assertions:
    - The `TestClass` has an attribute `_key_handler`.
    - The key code 65 (ASCII for 'A') is registered in `_key_handler`.
    - The key code 66 (ASCII for 'B') is registered in `_key_handler`.
    - The method `handle_a` is correctly mapped to key code 65 in `_key_handler`.
    - The method `handle_b` is correctly mapped to key code 66 in `_key_handler`.
    """

    @init
    class TestClass:
        @register(65)  # ASCII for 'A'
        def handle_a(self):
            return "Handled A"

        @register(66)  # ASCII for 'B'
        def handle_b(self):
            return "Handled B"

    assert hasattr(TestClass, "_key_handler")
    assert 65 in TestClass._key_handler
    assert 66 in TestClass._key_handler
    assert TestClass._key_handler[65] == TestClass.handle_a
    assert TestClass._key_handler[66] == TestClass.handle_b


def test_handle_input():
    """
    Test the handle_input method of TestClass.

    This test verifies that the handle_input method correctly handles
    different key inputs by using the `patch` decorator to mock the
    `bullet.utils.getchar` function.

    The test covers the following cases:
    - When the input is 'A' (ASCII 65), the method should return "Handled A".
    - When the input is 'B' (ASCII 66), the method should return "Handled B".
    - When the input is an undefined key, the method should return None.
    """

    @init
    class TestClass:
        @register(65)  # ASCII for 'A'
        def handle_a(self):
            return "Handled A"

        @register(66)  # ASCII for 'B'
        def handle_b(self):
            return "Handled B"

    instance = TestClass()

    with patch("bullet.utils.getchar", return_value="A"):
        result = instance.handle_input()
        assert result == "Handled A"

    with patch("bullet.utils.getchar", return_value="B"):
        result = instance.handle_input()
        assert result == "Handled B"

    with patch("bullet.utils.getchar", return_value=UNDEFINED_KEY):
        result = instance.handle_input()
        assert result is None


def test_handle_input_undefined_key():
    """
    Test the handle_input method of TestClass when an undefined key is pressed.

    This test verifies that the handle_input method returns None when an undefined key is pressed.
    It uses the `patch` decorator to mock the `bullet.utils.getchar` function to simulate key presses.

    Test Scenarios:
    1. When the 'C' key (ASCII 67) is pressed, which is not registered, the method should return None.
    2. When an undefined key (represented by UNDEFINED_KEY) is pressed, the method should return None.

    The TestClass is initialized with a handler for the 'A' key (ASCII 65), but this handler is not
    triggered in this test.
    """

    @init
    class TestClass:
        @register(65)  # ASCII for 'A'
        def handle_a(self):
            return "Handled A"

    instance = TestClass()

    with patch("bullet.utils.getchar", return_value="C"):
        result = instance.handle_input()
        assert result is None

    with patch("bullet.utils.getchar", return_value=UNDEFINED_KEY):
        result = instance.handle_input()
        assert result is None
