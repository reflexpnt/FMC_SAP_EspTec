# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-08-08 19:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repuestos', '0029_auto_20180808_1957'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articulo',
            name='marca',
            field=models.CharField(blank=True, default='', max_length=40),
        ),
        migrations.AlterField(
            model_name='articulo',
            name='modelo_NumParte',
            field=models.CharField(blank=True, default='', max_length=40),
        ),
    ]
