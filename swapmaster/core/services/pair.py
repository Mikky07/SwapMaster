from swapmaster.core.models import MethodId, CommissionId, Pair, CourseId, WalletId


class PairService:
    def create_pair(
        self,
        method_from: MethodId,
        method_to: MethodId,
        commission: CommissionId,
        course_id: CourseId,
        wallet_id: WalletId
    ) -> Pair:
        return Pair(
            id=None,
            method_from=method_from,
            method_to=method_to,
            commission=commission,
            course_id=course_id,
            reception_wallet=wallet_id
        )
