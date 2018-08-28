# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-08-28 14:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repuestos', '0044_articulo_sys_locked'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articulo',
            name='SYS_ESTADO',
            field=models.CharField(choices=[('Aprobado', 'Aprobado'), ('enRevision', 'enRevisión'), ('Cerrado', 'Cerrado'), ('enEdicion', 'en Edición'), ('Inicial', 'Inicial')], default='Inicial', max_length=10),
        ),
    ]
