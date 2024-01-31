from __future__ import annotations

from dataclasses import dataclass
from typing import NewType

UserId = NewType("UserId", int)


@dataclass
class User:
    user_id: UserId
    username: str
    hashed_password: str
