from dataclasses import dataclass


@dataclass
class Token:
    token_type: str
    access_token: str
