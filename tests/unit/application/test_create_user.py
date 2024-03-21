import pytest
from unittest.mock import Mock

from swapmaster.core.constants import VerificationStatusEnum
from swapmaster.core.models import User, UserId
from swapmaster.core.services import UserService
from swapmaster.application.create_user import CreateUser, NewUserDTO
from tests.mocks import UoWMock, VerifierMock
from tests.mocks.user import UserGatewayMock

TEST_USERNAME = "username"
TEST_EMAIL = "email"
TEST_PASSWORD = "password"
TEST_HASHED_PASSWORD = "hashed_password"
TEST_VERIFICATION_STATUS = VerificationStatusEnum.UNVERIFIED


@pytest.fixture
def user_service() -> Mock:
    user_service = Mock()

    user_service.create_user = Mock(
        return_value=User(
            id=None,
            username=TEST_USERNAME,
            email=TEST_EMAIL,
            hashed_password=TEST_HASHED_PASSWORD,
            verification_status=TEST_VERIFICATION_STATUS
        )
    )

    return user_service


@pytest.mark.asyncio
async def test_create_user_(
        uow: UoWMock,
        user_service: UserService,
        user_gateway: UserGatewayMock,
        verifier: VerifierMock
):
    new_user = NewUserDTO(
        username=TEST_USERNAME,
        email=TEST_EMAIL,
        password=TEST_PASSWORD
    )

    user_creator = CreateUser(
        uow=uow,
        user_service=user_service,
        user_gateway=user_gateway,
        verifier=verifier
    )

    created_user = await user_creator(data=new_user)

    assert type(created_user.id) is UserId
    assert created_user.hashed_password == TEST_HASHED_PASSWORD
    assert created_user.email == TEST_EMAIL
    assert created_user.verification_status == TEST_VERIFICATION_STATUS

    assert uow.committed
    assert verifier.verification_started
