# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-08-16 20:05
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('repuestos', '0041_auto_20180814_1540'),
    ]

    operations = [
        migrations.AddField(
            model_name='articulo',
            name='SYS_dataEntryAuthor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='data_entries', to=settings.AUTH_USER_MODEL),
        ),
    ]
