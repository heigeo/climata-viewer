from wq.db.contrib.chart.views import ChartView
from .models import DataRequest
from locations.models import Site
from wq.db.contrib.vera.models import Event, Report, Parameter


class ExportView(ChartView):
    def filter_by_extra(self, qs, extra):
        dr = DataRequest.objects.get(pk=extra[0])
        events = Event.objects.filter(
            report__in=Report.objects.filter_by_related(dr)
        )
        return qs.filter(event_id__in=events)

    def transform_dataframe(self, df):
        """
        Add site metadata to columns to make output more usable.
        """
        columns = []
        for col in df.columns:
            val, unit, pid, sid = col
            param = Parameter.objects.get_by_identifier(pid)
            site = Site.objects.get_by_identifier(sid)
            col = (
                val, unit, param.name,
                sid, site.name or '-',
                site.latitude or '-', site.longitude or '-'
            )
            columns.append(col)
        df.columns = df.columns.from_tuples(columns)
        df.columns.names = (
            "", "units", "parameter",
            "site id", "site name", "latitude", "longitude"
        )
        return df
