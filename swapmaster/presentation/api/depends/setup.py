import logging
from functools import partial

from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from swapmaster.adapters.db.gateways.currency import CurrencyGateway
from swapmaster.application.calculate_send_total import CalculateSendTotal
from swapmaster.application.common.protocols.course_obtainer import CourseObtainer
from swapmaster.application.common.protocols.commission_gateway import (
    CommissionWriter,
    CommissionReader
)
from swapmaster.application.common.protocols.method_gateway import MethodWriter, MethodListReader
from swapmaster.application.common.protocols.order_gateway import OrderWriter, OrderReader, OrderUpdater
from swapmaster.application.common.protocols.pair_gateway import PairReader, PairWriter
from swapmaster.application.common.protocols.currency_gateway import CurrencyListReader
from swapmaster.application.common.protocols.user_gateway import UserReader
from swapmaster.application.create_commission import AddCommission
from swapmaster.application.create_method import AddMethod
from swapmaster.application.common.uow import UoW
from swapmaster.application.create_order import AddOrder
from swapmaster.application.create_pair import AddPair
from swapmaster.application.finish_order import FinishOrder
from swapmaster.core.services.commission import CommissionService
from swapmaster.core.services.method import MethodService
from swapmaster.core.services.order import OrderService
from swapmaster.core.services.pair import PairService
from swapmaster.presentation.api.config.models.auth import AuthConfig
from swapmaster.presentation.api.config.models.main import APIConfig
from swapmaster.presentation.api.depends.auth import AuthProvider
from swapmaster.presentation.api.depends.providers import (
    new_order_gateway,
    new_uow,
    new_db_session,
    new_pair_gateway,
    new_currency_gateway,
    new_method_gateway,
    new_commission_gateway,
    new_course_obtainer_gateway,
    new_user_gateway
)

logger = logging.getLogger(__name__)


def set_depends_as_defaults(cls: type) -> None:
    init = cls.__init__
    args_count = init.__code__.co_kwonlyargcount + init.__code__.co_argcount - 1
    init.__defaults__ = tuple(
        Depends() for _ in range(args_count)
    )


def setup_dependencies(
    app: FastAPI,
    pool: async_sessionmaker[AsyncSession],
    config: APIConfig
):
    method_service = MethodService()
    commission_service = CommissionService()
    order_service = OrderService()
    pair_service = PairService()

    app.dependency_overrides.update(
        {
            MethodWriter: new_method_gateway,
            MethodListReader: new_method_gateway,
            CommissionWriter: new_commission_gateway,
            CommissionReader: new_commission_gateway,
            OrderWriter: new_order_gateway,
            OrderReader: new_order_gateway,
            OrderUpdater: new_order_gateway,
            CurrencyGateway: new_currency_gateway,
            CurrencyListReader: new_currency_gateway,
            PairReader: new_pair_gateway,
            PairWriter: new_pair_gateway,
            UserReader: new_user_gateway,
            CourseObtainer: new_course_obtainer_gateway,
            AsyncSession: partial(new_db_session, pool),
            AuthConfig: lambda: config.auth,
            PairService: lambda: pair_service,
            MethodService: lambda: method_service,
            CommissionService: lambda: commission_service,
            OrderService: lambda: order_service,
            UoW: new_uow,
        }
    )

    set_depends_as_defaults(AddMethod)
    set_depends_as_defaults(AddCommission)
    set_depends_as_defaults(AddOrder)
    set_depends_as_defaults(CalculateSendTotal)
    set_depends_as_defaults(AddPair)
    set_depends_as_defaults(AuthProvider)
    set_depends_as_defaults(FinishOrder)

    logger.info("dependencies set up!")
