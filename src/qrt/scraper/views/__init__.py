import json

from quart import Blueprint, session

from qrt.utils.constants import DEFAULT_SCRAPER_OPTIONS

from .scraper import ScraperView
from .options import OptionsView


bp = Blueprint("scraper", __name__, url_prefix="/scraper")

bp.add_url_rule("", "scraper", ScraperView.as_view("scraper"))
bp.add_url_rule("/options", "options", OptionsView.as_view("options"))

@bp.before_app_request
def set_user_default_options():
    if not session.get("options"):
        session["options"] = DEFAULT_SCRAPER_OPTIONS
