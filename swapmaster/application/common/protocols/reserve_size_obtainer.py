from dataclasses import dataclass
from typing import Protocol
from abc import abstractmethod

from swapmaster.core.models import ReserveId


@dataclass
class ReserveSize:
    reserve_id: ReserveId
    size: float


@dataclass
class RemoteReserve:
    reserve_id: ReserveId
    wallet_address: str


class ReserveSizeObtainer(Protocol):
    @abstractmethod
    async def obtain_reserves_sizes(self, reserves: list[RemoteReserve]) -> list[ReserveSize]:
        raise NotImplementedError
