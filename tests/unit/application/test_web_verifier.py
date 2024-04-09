import pytest

from swapmaster.core.constants import VerificationStatusEnum
from swapmaster.core.models import User, UserId
from swapmaster.core.utils.exceptions import VerificationFailed
from swapmaster.application.web_verifier import WebVerifier
from tests.mocks import (
    NotifierMock,
    UserGatewayMock,
    VerificationCashMock, UoWMock
)


TEST_USER_ID = UserId(0)
FAKE_VERIFICATION_CODE = "random_code"
TEST_USER = User(
    id=TEST_USER_ID,
    username="",
    hashed_password="",
    email="",
    verification_status=VerificationStatusEnum.UNVERIFIED,
    tg_id=None
)


@pytest.mark.asyncio
async def test_web_verifier_start_verification(
        notifier: NotifierMock,
        user_gateway: UserGatewayMock,
        verification_cash: VerificationCashMock,
        uow: UoWMock
):
    web_verifier = WebVerifier(
        notifier=notifier,
        cash=verification_cash,
        uow=uow,
        user_gateway=user_gateway
    )
    user_gateway.users[TEST_USER.id] = TEST_USER

    await web_verifier.start_verification(user=TEST_USER)

    saved_code = await verification_cash.get_code(user_id=TEST_USER.id)

    notifier.notified = False

    with pytest.raises(VerificationFailed):
        await web_verifier.finish_verification(user=TEST_USER, verification_code=FAKE_VERIFICATION_CODE)

    verified_user = await web_verifier.finish_verification(user=TEST_USER, verification_code=saved_code)

    assert verified_user.verification_status == VerificationStatusEnum.VERIFIED
    assert not verification_cash.codes.get(saved_code, False)
