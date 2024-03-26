from abc import ABC


class AppExtension(ABC):
    """
    Base class for app extensions. Must contain an `init_app` method.
    """

    def init_app(self, app) -> None:
        """
        Initialize the app extension.
        """
        raise NotImplementedError
