class WebexAssistantSDKException(Exception):
    pass


class EncryptionKeyError(WebexAssistantSDKException):
    pass


class SignatureGenerationError(WebexAssistantSDKException):
    pass


class RequestValidationError(WebexAssistantSDKException):
    """An exception raised when request is invalid"""

    pass


class SignatureValidationError(RequestValidationError):
    """An exception raised when signature validation fails"""

    pass


class ServerChallengeValidationError(RequestValidationError):
    pass


class ResponseValidationError(WebexAssistantSDKException):
    pass


class ClientChallengeValidationError(ResponseValidationError):
    pass
