import importlib

from quart import Blueprint

# types
from qrt.types import App


def register_blueprints(app: App):
    """
    Register all blueprints in the app.
    """
    for bundle in app.config["BUNDLES"]:
        module = importlib.import_module(f"{bundle}")
        # scan module for Blueprint instances
        for attribute_name in dir(module):
            attribute = getattr(module, attribute_name)
            if isinstance(attribute, Blueprint):
                app.logger.info(f"Registering blueprint: {attribute_name}")
                app.register_blueprint(attribute)
