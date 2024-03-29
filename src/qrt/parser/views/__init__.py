import json

from quart import Blueprint, session

from qrt.utils.constants import DEFAULT_PARSER_OPTIONS

from .parser import ParserView
from .options import OptionsView


bp = Blueprint("parser", __name__, url_prefix="/parser")


@bp.before_app_request
def set_user_default_options():
    if not session.get("options"):
        session["options"] = DEFAULT_PARSER_OPTIONS


bp.add_url_rule("/", "parser", ParserView.as_view("parser"))
bp.add_url_rule("/options", "options", OptionsView.as_view("options"))
