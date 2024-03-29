from quart import render_template
from quart.views import MethodView


class IndexView(MethodView):
    async def get(self):
        return await render_template("site/index/page.html", tab="Home")
