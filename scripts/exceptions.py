"""
    Define here every custom exceptions for this project
"""


class AppError(Exception):
    """Causes the whole app to crash"""


class BadlyFormedJSON(Exception):
    """Raised when the given JSON file is badly written"""


class NeighborNotLinked(Exception):
    pass
