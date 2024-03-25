class ValidationError(Exception):
    """
    Exception raised for errors in the input.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, variable: str, expected: str, actual: str):
        self.message = f"Expected {variable} to be {expected}, but got {actual}."
        super().__init__(self.message)
