from dataclasses import dataclass


@dataclass(slots=True)
class Token:
    token_type: str
    access_token: str
