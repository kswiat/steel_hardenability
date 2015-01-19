# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('metal', '0002_auto_20150118_1348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='steel',
            name='carbon',
            field=models.FloatField(default=0.1, verbose_name='carbon', validators=[django.core.validators.MinValueValidator(0.1), django.core.validators.MaxValueValidator(0.7)]),
            preserve_default=True,
        ),
    ]
