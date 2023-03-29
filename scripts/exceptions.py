"""
    Define here every custom exceptions for this project
"""


class AppError(Exception):
    """Causes the whole app to crash"""


class NeighborNotLinked(Exception):
    pass
