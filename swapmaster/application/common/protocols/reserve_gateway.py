from abc import abstractmethod
from typing import Protocol

from swapmaster.core.models.reserve import Reserve, ReserveId
from swapmaster.core.models.wallet import WalletId
from swapmaster.application.common.protocols.reserve_size_obtainer import RemoteReserve


class ReserveWriter(Protocol):
    @abstractmethod
    async def add_reserve(self, reserve: Reserve) -> Reserve:
        raise NotImplementedError


class ReserveUpdater(Protocol):
    @abstractmethod
    async def attach_wallet(self, wallet_id: WalletId, reserve_id: ReserveId) -> Reserve:
        raise NotImplementedError

    @abstractmethod
    async def update_reserve_size(self, reserve_id: ReserveId, size: float) -> Reserve:
        raise NotImplementedError


class ReserveReader(Protocol):
    @abstractmethod
    async def get_all_remote_reserves(self) -> list[RemoteReserve]:
        raise NotImplementedError
