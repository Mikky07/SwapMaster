import logging
from functools import partial

from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from swapmaster.adapters.db.gateways.order import OrderGateway
from swapmaster.adapters.verification import EmailNotifier
from swapmaster.application.common.db import *
from swapmaster.application import *
from swapmaster.application.common import *
from swapmaster.application.verifier import Verifier
from swapmaster.core.services import *
from swapmaster.adapters.db.gateways import *
from swapmaster.presentation.api.config.models.auth import AuthConfig
from swapmaster.presentation.api.config.models.main import APIConfig
from swapmaster.presentation.api.depends.auth import AuthProvider
from swapmaster.presentation.api.depends.providers import (
    new_uow,
    new_db_session,
    DBGatewayProvider
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
    requisite_service = RequisiteService()
    user_service = UserService()
    email_notifier = EmailNotifier()

    app.dependency_overrides.update(
        {
            MethodWriter: DBGatewayProvider(MethodGateway),
            MethodListReader: DBGatewayProvider(MethodGateway),
            CommissionWriter: DBGatewayProvider(CommissionGateway),
            CommissionReader: DBGatewayProvider(CommissionGateway),
            UserSaver: DBGatewayProvider(UserGateway),
            OrderWriter: DBGatewayProvider(OrderGateway),
            OrderReader: DBGatewayProvider(OrderGateway),
            OrderUpdater: DBGatewayProvider(OrderGateway),
            RequisiteWriter: DBGatewayProvider(RequisiteGateway),
            RequisiteReader: DBGatewayProvider(RequisiteGateway),
            ReserveUpdater: DBGatewayProvider(ReserveGateway),
            ReserveReader: DBGatewayProvider(ReserveGateway),
            OrderRequisiteReader: DBGatewayProvider(OrderRequisiteGateway),
            OrderRequisiteWriter: DBGatewayProvider(OrderRequisiteGateway),
            CurrencyGateway: DBGatewayProvider(CurrencyGateway),
            CurrencyListReader: DBGatewayProvider(CurrencyGateway),
            PairReader: DBGatewayProvider(PairGateway),
            PairWriter: DBGatewayProvider(PairGateway),
            UserReader: DBGatewayProvider(UserGateway),
            AsyncSession: partial(new_db_session, pool),
            AuthConfig: lambda: config.auth,
            PairService: lambda: pair_service,
            MethodService: lambda: method_service,
            CommissionService: lambda: commission_service,
            OrderService: lambda: order_service,
            RequisiteService: lambda: requisite_service,
            UserService: lambda: user_service,
            Notifier: lambda: email_notifier,
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
    set_depends_as_defaults(AddRequisite)
    set_depends_as_defaults(GetFullOrder)
    set_depends_as_defaults(CancelOrder)
    set_depends_as_defaults(Authenticate)
    set_depends_as_defaults(Verifier)

    logger.info("dependencies set up!")
