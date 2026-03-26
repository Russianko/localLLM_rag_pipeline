class AppError(Exception):
    pass


class DocumentNotFoundError(AppError):
    pass


class DocumentNotProcessedError(AppError):
    pass


class InvalidRequestError(AppError):
    pass