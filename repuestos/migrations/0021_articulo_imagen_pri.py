# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-08-06 18:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repuestos', '0020_remove_image_art_pri_descripcion'),
    ]

    operations = [
        migrations.AddField(
            model_name='articulo',
            name='imagen_pri',
            field=models.ImageField(default='./no_image.png', upload_to='./pic_folder/'),
        ),
    ]
