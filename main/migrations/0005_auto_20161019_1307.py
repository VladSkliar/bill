# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-19 13:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20161019_1204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='image',
            field=models.ImageField(blank=True, upload_to='bills/img/', verbose_name='\u041a\u0430\u0440\u0442\u0438\u043d\u043a\u0430'),
        ),
    ]