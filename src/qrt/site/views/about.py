from quart import render_template
from quart.views import MethodView


class AboutView(MethodView):
    async def get(self):
        return await render_template("site/about/page.html", tab="About")
