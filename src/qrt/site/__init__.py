from quart import Blueprint

from qrt.site import views

site = Blueprint("site", __name__)

site.add_url_rule("/", "index", views.index)
