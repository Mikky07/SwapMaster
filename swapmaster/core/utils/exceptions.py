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


class AlreadyExists(SMError):
    pass
