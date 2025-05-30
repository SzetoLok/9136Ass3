class CustomValueError(Exception):
    """
    This error should be raised when the value isn't what its expected to be.
    """
    def __init__(self, message="CustomValueError occurred"):
        # print(message)
        super().__init__(message)

class CustomTypeError(Exception):
    """
    This error should be raised when the type of the value isn't what its expected to be.
    """
    def __init__(self, message="CustomTypeError occurred"):
        # print(message)
        super().__init__(message)

class CustomAttributeError(Exception):
    """
    This error should be raised when the attribute doesn't exist as expected
    """
    def __init__(self, message="CustomAttributeError occurred"):
        # print(message)
        super().__init__(message)

class CustomKeyError(Exception):
    """
    This error should be raised when a key is expected to exist in a dictionary but doesn't exist.
    """
    def __init__(self, message="CustomKeyError occurred"):
        # print(message)
        super().__init__(message)

class CustomOperationError(Exception):
    """
    Raised when an operation is not allowed (e.g., on a banned account).
    """
    def __init__(self, message="CustomOperationError occurred"):
        # print(message)
        super().__init__(message)

class CustomLimitError(Exception):
    """
    Raised when a transaction exceeds the allowed limit.
    """
    def __init__(self, message="CustomLimitError occurred"):
        # print(message)
        super().__init__(message)
