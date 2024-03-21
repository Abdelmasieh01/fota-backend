class SignatureValidationError(BaseException):
    """Exception raised when signature validation fails."""
    def __init__(self, message="Signature validation failed"):
        self.message = message
        super().__init__(self.message)