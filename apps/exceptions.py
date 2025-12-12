# apps/exceptions.py

class AppError(Exception):
    """Base app-level exception with an HTTP status and message."""
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class LLMError(AppError):
    """Raised when LLM call fails or returns invalid output."""
    def __init__(self, message: str = "Error while calling LLM"):
        super().__init__(message, status_code=502)


class SQLGenerationError(AppError):
    """Raised when generated SQL is invalid / unusable."""
    def __init__(self, message: str = "Failed to generate valid SQL"):
        super().__init__(message, status_code=400)


class QueryExecutionError(AppError):
    """Raised when SQL execution on DB fails."""
    def __init__(self, message: str = "Error while executing SQL query"):
        super().__init__(message, status_code=500)


class NoDataFoundError(AppError):
    """Raised when query returns empty result but data was expected."""
    def __init__(self, message: str = "No data found for the given query"):
        super().__init__(message, status_code=404)
