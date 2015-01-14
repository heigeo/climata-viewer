# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0001_initial'),
        ('vera', '0002_result'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventResult',
            fields=[
                ('id', models.PositiveIntegerField(serialize=False, primary_key=True)),
                ('event_type', models.CharField(max_length=10, null=True, blank=True)),
                ('event_date', models.DateField()),
                ('result_value_numeric', models.FloatField(null=True, blank=True)),
                ('result_value_text', models.TextField(null=True, blank=True)),
                ('result_empty', models.BooleanField(default=False)),
                ('event', models.ForeignKey(to=settings.WQ_EVENT_MODEL)),
                ('event_site', models.ForeignKey(null=True, to=settings.WQ_SITE_MODEL, blank=True)),
                ('result', models.ForeignKey(to=settings.WQ_RESULT_MODEL)),
                ('result_report', models.ForeignKey(to=settings.WQ_REPORT_MODEL)),
                ('result_type', models.ForeignKey(to=settings.WQ_PARAMETER_MODEL)),
            ],
            options={
                'db_table': 'wq_eventresult',
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='eventresult',
            unique_together=set([('event', 'result_type')]),
        ),
    ]
