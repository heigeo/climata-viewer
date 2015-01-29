from wq.db.rest import app
from django.conf import settings
from .views import Home

app.router.add_page('index', {'url': ''}, Home)
app.router.add_page('about', {'url': 'about'})
app.router.set_extra_config(
    color_names=settings.COLOR_NAMES,
    hex_colors=settings.HEX_COLORS,
)
