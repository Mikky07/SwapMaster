from abc import ABC

from swapmaster.presentation.interactor_factory import InteractorFactory


class BotInteractorFactory(InteractorFactory, ABC):
    """This abc extends base interactor factory ABC with according to tgbot specificity"""
    ...
