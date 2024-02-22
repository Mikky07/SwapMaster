from swapmaster.core.models import MethodId, CommissionId, Pair, CourseId


class PairService:
    def create_pair(
        self,
        method_from: MethodId,
        method_to: MethodId,
        commission: CommissionId,
        course_id: CourseId
    ) -> Pair:
        return Pair(
            id=None,
            method_from=method_from,
            method_to=method_to,
            commission=commission,
            course_id=course_id
        )
