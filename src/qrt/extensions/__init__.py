import importlib

# types
from .base import AppExtension
from qrt.types import App


def init_extensions(app: App):
    """
    Initialize all extensions.
    """
    extensions: list[AppExtension] = []

    for extension_name in app.config["EXTENSIONS"]:
        module = importlib.import_module(f"qrt.extensions.{extension_name}")
        # scan module for BaseAppExtension instances
        for attribute_name in dir(module):
            attribute = getattr(module, attribute_name)
            # check if attribute as init_app method
            if attribute_name in app.config["EXTENSIONS"]:
                app.logger.info(f"Initializing extension: {attribute_name}")
                extensions.append(attribute)

    for extension in extensions:
        extension.init_app(app=app)
