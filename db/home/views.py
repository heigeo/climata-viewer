from rest_framework.response import Response
from wq.db.rest.views import SimpleViewSet
from wq.db.rest import app
from data.models import Project


class Home(SimpleViewSet):
    template_name = "index.html"

    def list(self, request, *args, **kwargs):
        project = Project.objects.filter(
            public=True
        ).order_by('-created')[0]
        return Response({
            'latest_project': app.router.serialize(project)
        })
