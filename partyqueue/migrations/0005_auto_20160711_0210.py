# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-11 06:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partyqueue', '0004_auto_20160711_0207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='queueitem',
            name='place_in_line',
            field=models.IntegerField(blank=True),
        ),
    ]