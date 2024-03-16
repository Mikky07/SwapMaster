from dataclasses import dataclass


@dataclass
class AuthConfig:
    secret_key: str
    expire_minutes: int
