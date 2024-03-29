from uuid import uuid4

from quart import Quart, session
from dotenv import load_dotenv

from qrt.magic import register_blueprints
from qrt.extensions import init_extensions

# types
from .types import Mode, App

load_dotenv()


def create_app(mode: Mode) -> App:
    """
    Create a new Quart app with the given configuration.
    """
    app = Quart(__name__)
    app.config.from_object(f"qrt.config.{mode.capitalize()}Config")

    init_extensions(app)
    register_blueprints(app)

    return app
