class APIConnectionError(Exception):
    """Custom exception for API connection errors."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"APIConnectionError: {self.message}"
