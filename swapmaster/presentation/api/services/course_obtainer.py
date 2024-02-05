from swapmaster.core.constants import CourseObtainingMethod
from swapmaster.application.common.course_obtainer import CourseObtainer
from swapmaster.adapters.course_obtaining.static_method_gateway import StaticCourseObtainerGateway


# stub
def choose_course_obtainer(method: CourseObtainingMethod) -> CourseObtainer:
    if method == CourseObtainingMethod.STOCK_EXCHANGE_SERVICE:
        return ...
    return StaticCourseObtainerGateway()
