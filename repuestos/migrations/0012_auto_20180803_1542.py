# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-08-03 15:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repuestos', '0011_auto_20180803_1539'),
    ]

    operations = [
        migrations.AlterField(
            model_name='archivo',
            name='archivo1',
            field=models.FileField(upload_to='./'),
        ),
    ]
