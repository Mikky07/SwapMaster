from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, TypeAlias

from swapmaster.core.constants import VerificationStatusEnum

UserId: TypeAlias = int


@dataclass
class User:
    id: Optional[UserId]
    username: str
    email: str
    hashed_password: str
    verification_status: VerificationStatusEnum
