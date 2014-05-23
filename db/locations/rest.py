from .models import Site
from wq.db.rest import app

app.router.register_model(Site)
