from __future__ import annotations

from dataclasses import dataclass
from typing import TypeAlias

from swapmaster.core.constants import VerificationStatusEnum

UserId: TypeAlias = int


@dataclass(slots=True)
class User:
    id: UserId | None
    username: str
    tg_id: int | None
    email: str | None
    hashed_password: str | None
    verification_status: VerificationStatusEnum
