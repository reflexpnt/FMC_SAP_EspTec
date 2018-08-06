# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-08-03 18:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repuestos', '0015_auto_20180803_1651'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image_Art_pri',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('descripcion', models.CharField(blank=True, max_length=255)),
                ('image', models.ImageField(default='./no_image.png', max_length=254, upload_to='./')),
            ],
        ),
        migrations.DeleteModel(
            name='Archivo',
        ),
    ]
