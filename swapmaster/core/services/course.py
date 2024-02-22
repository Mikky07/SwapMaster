from swapmaster.core.models import Course


class CourseService:
    def create_course(
            self,
            update_method,
            value
    ) -> Course:
        return Course(
            id=None,
            update_method=update_method,
            value=value
        )
