from quart import Blueprint

from .index import IndexView
from .about import AboutView


bp = Blueprint("site", __name__)

bp.add_url_rule("/", "index", IndexView.as_view("index"))
bp.add_url_rule("/about", "about", AboutView.as_view("about"))
