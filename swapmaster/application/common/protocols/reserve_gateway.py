from abc import abstractmethod
from typing import Protocol

from swapmaster.application.common.reserve_refresh import RemoteReserve
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


class ReserveReader(Protocol):
    @abstractmethod
    async def get_all_remote_reserves(self) -> RemoteReserve:
        raise NotImplementedError
