# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('metal', '0004_auto_20150118_1916'),
    ]

    operations = [
        migrations.AlterField(
            model_name='steel',
            name='carbon',
            field=models.FloatField(default=0.1, help_text='0.1 - 0.9', verbose_name='carbon', validators=[django.core.validators.MinValueValidator(0.1), django.core.validators.MaxValueValidator(0.9)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='steel',
            name='chromium',
            field=models.FloatField(default=0, help_text='0 - 1.75', verbose_name='chromium', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1.75)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='steel',
            name='manganese',
            field=models.FloatField(default=0, help_text='0 - 1.95', verbose_name='manganese', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1.95)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='steel',
            name='molybdenum',
            field=models.FloatField(default=0, help_text='0 - 0.55', verbose_name='molybdenum', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(0.55)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='steel',
            name='nickel',
            field=models.FloatField(default=0, help_text='0 - 2', verbose_name='nickel', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(2)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='steel',
            name='silicon',
            field=models.FloatField(default=0, help_text='0 - 2', verbose_name='silicon', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(2)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='steel',
            name='vanadium',
            field=models.FloatField(default=0, help_text='0 - 0.2', verbose_name='vanadium', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(0.2)]),
            preserve_default=True,
        ),
    ]
