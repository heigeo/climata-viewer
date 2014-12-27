# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('identify', '0001_initial'),
        migrations.swappable_dependency(settings.WQ_PARAMETER_MODEL),
        migrations.swappable_dependency(settings.WQ_REPORT_MODEL),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        migrations.swappable_dependency(settings.WQ_RESULT_MODEL),
        migrations.swappable_dependency(settings.WQ_SITE_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DataRequest',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('requested', models.DateTimeField(auto_now_add=True)),
                ('completed', models.DateTimeField(null=True, blank=True)),
                ('deleted', models.DateTimeField(null=True, blank=True)),
                ('public', models.BooleanField(default=False)),
                ('start_date', models.DateField(null=True, blank=True)),
                ('end_date', models.DateField(null=True, blank=True)),
                ('user', models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL, blank=True)),
            ],
            options={
                'ordering': ('-requested',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('type', models.CharField(max_length=10, null=True, blank=True)),
                ('date', models.DateField()),
                ('site', models.ForeignKey(null=True, related_name='event_set', to=settings.WQ_SITE_MODEL, blank=True)),
            ],
            options={
                'ordering': ('-date', 'type'),
            },
            bases=(models.Model,),
        ),
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
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('deleted', models.DateTimeField(null=True, blank=True)),
                ('public', models.BooleanField(default=False)),
                ('user', models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Webservice',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('homepage', models.URLField()),
                ('class_name', models.CharField(max_length=255)),
                ('authority', models.ForeignKey(to='identify.Authority')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='eventresult',
            unique_together=set([('event', 'result_type')]),
        ),
        migrations.AlterUniqueTogether(
            name='event',
            unique_together=set([('site', 'date', 'type')]),
        ),
        migrations.AddField(
            model_name='datarequest',
            name='webservice',
            field=models.ForeignKey(to='data.Webservice'),
            preserve_default=True,
        ),
    ]
