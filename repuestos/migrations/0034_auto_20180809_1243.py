# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-08-09 12:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repuestos', '0033_auto_20180808_2008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articulo',
            name='Descripcion',
            field=models.TextField(blank=True, default='', max_length=500),
        ),
        migrations.AlterField(
            model_name='articulo',
            name='Ensayos',
            field=models.TextField(blank=True, default='', max_length=500),
        ),
    ]
