from wq.db.contrib.chart.views import ChartView
from .models import DataRequest
from wq.db.contrib.vera.models import Event, Report


class ExportView(ChartView):
    def filter_by_extra(self, qs, extra):
        dr = DataRequest.objects.get(pk=extra[0])
        events = Event.objects.filter(
            report__in=Report.objects.filter_by_related(dr)
        )
        return qs.filter(event_id__in=events)
