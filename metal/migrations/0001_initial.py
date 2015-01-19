# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Steel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('carbon', models.FloatField(default=0, verbose_name='carbon')),
                ('manganese', models.FloatField(default=0, verbose_name='manganese')),
                ('nickel', models.FloatField(default=0, verbose_name='nickel')),
                ('chromium', models.FloatField(default=0, verbose_name='chromium')),
                ('molybdenum', models.FloatField(default=0, verbose_name='molybdenum')),
                ('vanadium', models.FloatField(default=0, verbose_name='vanadium')),
                ('silicon', models.FloatField(default=0, verbose_name='vanadium')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
