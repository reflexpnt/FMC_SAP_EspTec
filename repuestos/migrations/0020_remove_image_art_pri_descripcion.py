# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-08-06 15:38
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('repuestos', '0019_auto_20180806_1534'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image_art_pri',
            name='descripcion',
        ),
    ]
