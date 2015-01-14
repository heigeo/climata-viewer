# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0002_eventresult'),
    ]

    operations = [
        migrations.AddField(
            model_name='webservice',
            name='description',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='webservice',
            name='slug',
            field=models.SlugField(default=''),
            preserve_default=False,
        ),
    ]
