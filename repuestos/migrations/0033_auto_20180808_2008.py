# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-08-08 20:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repuestos', '0032_remove_articulo_datasheet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articulo',
            name='Descripcion',
            field=models.TextField(blank=True, default=' ', max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='articulo',
            name='Ensayos',
            field=models.TextField(blank=True, default=' ', max_length=500),
        ),
    ]