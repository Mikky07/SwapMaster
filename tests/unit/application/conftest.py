from pytest import fixture

from tests.mocks import (
    UoWMock,
    AsyncTaskManagerMock,
    CentralConfigMock,
    RequisiteServiceMock
)

@fixture
def uow() -> UoWMock:
    return UoWMock()


@fixture
def requisite_service() -> RequisiteServiceMock:
    return RequisiteServiceMock()


@fixture
def central_config() -> CentralConfigMock:
    return CentralConfigMock()

@fixture
def async_task_manager() -> AsyncTaskManagerMock:
    return AsyncTaskManagerMock()
