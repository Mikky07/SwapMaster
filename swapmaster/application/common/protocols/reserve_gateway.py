from abc import abstractmethod
from typing import Protocol

from swapmaster.core.models.reserve import Reserve, ReserveId
from swapmaster.core.models.wallet import WalletId


class ReserveWriter(Protocol):
    @abstractmethod
    async def add_reserve(self, reserve: Reserve) -> Reserve:
        raise NotImplementedError


class ReserveUpdater(Protocol):
    @abstractmethod
    async def attach_wallet(self, wallet_id: WalletId, reserve_id: ReserveId) -> Reserve:
        raise NotImplementedError
