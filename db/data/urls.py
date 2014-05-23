from django.conf.urls import patterns, include, url
from rest_framework.urlpatterns import format_suffix_patterns
from wq.db.contrib.chart.urls import ids
from .views import ExportView

urlpatterns = patterns('',
    url(ids + r'/export$', ExportView.as_view()),
)
urlpatterns = format_suffix_patterns(urlpatterns)
