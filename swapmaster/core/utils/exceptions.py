class SMError(Exception):
    def __init__(
            self,
            text: str,
            *args,
            **kwargs,
    ) -> None:
        super().__init__(args, kwargs)
        self.text = text

    def __str__(self) -> str:
        error_text = "Error: " + self.text
        return error_text

    def __repr__(self) -> str:
        return (
            f"Error.\n"
            f"Type: {self.__class__.__name__}\n"
            f"text: {self.text}"
        )


class GatewayError(SMError):
    """This is the base error for gateways"""
    pass


class AuthFailed(SMError):
    pass


class VerificationFailed(SMError):
    pass


class OrderCreationError(SMError):
    pass


class RequisitesNotValid(SMError):
    pass


class AlreadyExists(SMError):
    pass


class UserNotFound(SMError):
    pass


class VerificationFailed(SMError):
    pass


class AlreadyVerified(SMError):
    pass


class NoReceptionWallet(SMError):
    pass


class PairNotUsable(SMError):
    pass


class CommissionIsNotValid(SMError):
    pass


class PairNotExists(SMError):
    pass


class RequisiteAlreadyExists(SMError):
    pass
