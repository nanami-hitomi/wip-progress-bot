class InvalidArgumentLengthError(Exception):
    """Raised when arguments are wrong length"""
    pass

class NoArgumentError(Exception):
    """Raised when no arguments provided when they should be"""
    pass

class NotMangaIDError(Exception):
    """Raised when a manga ID or nickname value is incorrect"""
    pass