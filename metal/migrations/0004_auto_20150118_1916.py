# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('metal', '0003_auto_20150118_1400'),
    ]

    operations = [
        migrations.CreateModel(
            name='IdealDiameter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.FloatField(default=0, verbose_name='value', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(500)])),
                ('grain', models.PositiveIntegerField(default=1, verbose_name='grain')),
                ('steel', models.ForeignKey(related_name='ideal_diameters', verbose_name='steel', to='metal.Steel')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='steel',
            name='carbon',
            field=models.FloatField(default=0.1, help_text='0.1 - 0.7', verbose_name='carbon', validators=[django.core.validators.MinValueValidator(0.1), django.core.validators.MaxValueValidator(0.7)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='steel',
            name='chromium',
            field=models.FloatField(default=0, help_text='0 - 3', verbose_name='chromium', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(3)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='steel',
            name='manganese',
            field=models.FloatField(default=0, help_text='0 - 3', verbose_name='manganese', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(3)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='steel',
            name='molybdenum',
            field=models.FloatField(default=0, help_text='0 - 1', verbose_name='molybdenum', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='steel',
            name='nickel',
            field=models.FloatField(default=0, help_text='0 - 3', verbose_name='nickel', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(3)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='steel',
            name='silicon',
            field=models.FloatField(default=0, help_text='0 - 2.3', verbose_name='silicon', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(2.3)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='steel',
            name='vanadium',
            field=models.FloatField(default=0, help_text='0 - 3', verbose_name='vanadium', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(3)]),
            preserve_default=True,
        ),
    ]
