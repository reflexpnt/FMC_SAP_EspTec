# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-07-30 16:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repuestos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='articulo',
            name='image',
            field=models.ImageField(default='no_image.png', upload_to=''),
        ),
    ]
