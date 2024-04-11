from dataclasses import dataclass
from typing import Tuple, Iterable

from swapmaster.application.common import Interactor, UoW
from swapmaster.application.common.gateways import PairReader
from swapmaster.core.models import MethodId, PairId, Course, Method, Commission


@dataclass
class AvailableTransferMethod:
    pair_id: PairId
    course_value: float
    method_from: Method


class GetAvailableTransferInformation(Interactor[MethodId, Iterable[AvailableTransferMethod]]):
    def __init__(
            self,
            uow: UoW,
            pair_gateway: PairReader
    ):
        self.uow = uow
        self.pair_gateway = pair_gateway

    async def __call__(self, method_to_id: MethodId) -> list[AvailableTransferMethod]:
        full_pair_info: list[
            Tuple[PairId, Commission, Method, Course]
        ] = await self.pair_gateway.get_pair_for_exchange(method_id=method_to_id)
        available_transfer_information = []
        for pair_id, commission, method_from, course in full_pair_info:
            course_with_commission = course.value + course.value * commission.value / 100
            available_transfer_information.append(
                AvailableTransferMethod(
                    pair_id=pair_id,
                    course_value=course_with_commission,
                    method_from=method_from
                )
            )
        print(available_transfer_information)
        return available_transfer_information
