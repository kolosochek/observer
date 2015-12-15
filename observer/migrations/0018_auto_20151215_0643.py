# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-15 03:43
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('observer', '0017_auto_20151214_1837'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accepted_eula', models.BooleanField()),
                ('department', models.CharField(default=b'', max_length=20)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='employee',
            name='default_view_mode',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ticket',
            name='ticket_update_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2015, 12, 15, 6, 42, 54, 557495)),
        ),
    ]