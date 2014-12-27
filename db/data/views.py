from wq.db.rest.views import ModelViewSet
from dbio.views import IoViewSet
from vera.views import ChartView
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import DataRequest
from locations.models import Site
from .models import Event
from vera.models import Report, Parameter
from django.utils.timezone import now


class ToggleViewSet(ModelViewSet):
    @action()
    def toggle(self, request, *args, **kwargs):
        self.retrieve(request, *args, **kwargs)
        obj = self.object
        if request.user == obj.user:
            obj.public = True if request.POST.get("public", None) else False
            obj.save()
        return Response({
            'public': obj.public
        })

    @action()
    def delete(self, request, *args, **kwargs):
        self.retrieve(request, *args, **kwargs)
        obj = self.object
        if request.user == obj.user:
            obj.deleted = now()
            obj.save()
            deleted = True
        else:
            deleted = False
        return Response({'deleted': deleted})


class DataRequestViewSet(IoViewSet, ToggleViewSet):
    @action()
    def auto(self, request, *args, **kwargs):
        response = super(DataRequestViewSet, self).auto(
            request, *args, **kwargs
        )
        links = [{
            'url': '/',
            'label': "Back to Home"
        }]
        obj = self.object
        project = obj.project
        if project:
            links.append({
                'url': '/projects/%s' % obj.get_object_id(project),
                'label': "Back to Project: %s" % project,
            })
        response.data['links'] = links
        return response


class ExportView(ChartView):
    def filter_by_extra(self, qs, extra):
        # Filter by datarequest: return the latest data for all events that
        # were affected by the datarequest.  (This is subtly different then
        # returning only the actual data imported by the request.)
        from .rest import user_filter
        reqs = user_filter(DataRequest.objects, self.request)
        if extra[0] == "latest":
            dr = reqs.filter(public=True).order_by('-completed')[0]
        else:
            dr = reqs.get(pk=extra[0])

        events = Event.objects.filter(
            report_set__in=Report.objects.filter_by_related(dr)
        )
        qs = qs.filter(event_id__in=events)
        if dr.parameter:
            rels = dr.inverserelationships.filter(
                from_content_type__name='parameter'
            )
            qs = qs.filter(result_type=rels[0].right)
        return qs

    def transform_dataframe(self, df):
        """
        Add site metadata to columns to make output more usable.
        """
        # Unstack event.type as a column instead of a row field
        df = df.unstack()

        columns = []
        for col in df.columns:
            val, unit, pid, sid, etype = col
            param = Parameter.objects.get_by_identifier(pid)
            site = Site.objects.get_by_identifier(sid)
            col = (
                val, unit, param.name,
                sid, site.name or '-',
                site.latitude or '-', site.longitude or '-',
                etype or "-",
            )
            columns.append(col)
        df.columns = df.columns.from_tuples(columns)
        df.columns.names = (
            "", "units", "parameter",
            "site id", "site name", "latitude", "longitude", "type",
        )
        return df
