# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-14 15:29
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('observer', '0014_auto_20151214_1829'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='ticket_update_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2015, 12, 14, 18, 29, 30, 352534)),
        ),
    ]
