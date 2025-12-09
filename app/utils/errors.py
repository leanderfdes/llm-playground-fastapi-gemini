# app/utils/errors.py
class LLMServiceError(Exception):
    """Custom exception for errors in the LLM service."""

    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(message)
