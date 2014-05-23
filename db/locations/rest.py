from .models import Site, Region
from wq.db.rest import app

app.router.register_model(Site)
app.router.register_model(Region, per_page=10000)
