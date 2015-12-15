# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-14 14:42
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('observer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('ticket_department', models.CharField(blank=True, max_length=254, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticket_department', models.CharField(blank=True, max_length=50, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='ticket',
            name='ticket_last_message',
            field=models.TextField(blank=True, max_length=8096, verbose_name=b'Ticket email'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='ticket_update_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2015, 12, 14, 17, 42, 10, 396108)),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='ticket_department',
            field=models.CharField(blank=True, choices=[(b'', b'All'), (b'\xd0\xa2\xd0\xb5\xd1\x85\xd0\xbd\xd0\xb8\xd1\x87\xd0\xb5\xd1\x81\xd0\xba\xd0\xb0\xd1\x8f \xd0\xbf\xd0\xbe\xd0\xb4\xd0\xb4\xd0\xb5\xd1\x80\xd0\xb6\xd0\xba\xd0\xb0', b'\xd0\xa2\xd0\xb5\xd1\x85\xd0\xbd\xd0\xb8\xd1\x87\xd0\xb5\xd1\x81\xd0\xba\xd0\xb0\xd1\x8f \xd0\xbf\xd0\xbe\xd0\xb4\xd0\xb4\xd0\xb5\xd1\x80\xd0\xb6\xd0\xba\xd0\xb0'), (b'\xd0\x94\xd0\xb5\xd0\xb6\xd1\x83\xd1\x80\xd0\xbd\xd1\x8b\xd0\xb9 \xd0\xb0\xd0\xb4\xd0\xbc\xd0\xb8\xd0\xbd\xd0\xb8\xd1\x81\xd1\x82\xd1\x80\xd0\xb0\xd1\x82\xd0\xbe\xd1\x80', b'\xd0\x94\xd0\xb5\xd0\xb6\xd1\x83\xd1\x80\xd0\xbd\xd1\x8b\xd0\xb9 \xd0\xb0\xd0\xb4\xd0\xbc\xd0\xb8\xd0\xbd\xd0\xb8\xd1\x81\xd1\x82\xd1\x80\xd0\xb0\xd1\x82\xd0\xbe\xd1\x80'), (b'\xd0\xa0\xd1\x83\xd0\xba\xd0\xbe\xd0\xb2\xd0\xbe\xd0\xb4\xd1\x81\xd1\x82\xd0\xb2\xd0\xbe', b'\xd0\xa0\xd1\x83\xd0\xba\xd0\xbe\xd0\xb2\xd0\xbe\xd0\xb4\xd1\x81\xd1\x82\xd0\xb2\xd0\xbe'), (b'\xd0\xa4\xd0\xb8\xd0\xbd.\xd0\xbe\xd1\x82\xd0\xb4\xd0\xb5\xd0\xbb', b'\xd0\xa4\xd0\xb8\xd0\xbd.\xd0\xbe\xd1\x82\xd0\xb4\xd0\xb5\xd0\xbb'), (b'\xd0\x96\xd0\xb0\xd0\xbb\xd0\xbe\xd0\xb1\xd1\x8b', b'\xd0\x96\xd0\xb0\xd0\xbb\xd0\xbe\xd0\xb1\xd1\x8b'), (b'\xd0\xa1\xd1\x82\xd0\xb0\xd1\x80\xd1\x88\xd0\xb8\xd0\xb9 \xd0\xb0\xd0\xb4\xd0\xbc\xd0\xb8\xd0\xbd\xd0\xb8\xd1\x81\xd1\x82\xd1\x80\xd0\xb0\xd1\x82\xd0\xbe\xd1\x80', b'\xd0\xa1\xd1\x82\xd0\xb0\xd1\x80\xd1\x88\xd0\xb8\xd0\xb9 \xd0\xb0\xd0\xb4\xd0\xbc\xd0\xb8\xd0\xbd\xd0\xb8\xd1\x81\xd1\x82\xd1\x80\xd0\xb0\xd1\x82\xd0\xbe\xd1\x80')], default=b'All', max_length=64, verbose_name=b'Ticket department'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='ticket_due',
            field=models.CharField(blank=True, max_length=64, verbose_name=b'Ticket due'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='ticket_email',
            field=models.CharField(blank=True, max_length=256, verbose_name=b'Ticket email'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='ticket_owner',
            field=models.CharField(blank=True, max_length=128, verbose_name=b'Ticket owner'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='ticket_priority',
            field=models.CharField(blank=True, choices=[(b'', b'All'), (b'low', b'Low'), (b'medium', b'Medium'), (b'high', b'High')], default=b'All', max_length=64, verbose_name=b'Ticket priority'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='ticket_replier',
            field=models.CharField(blank=True, max_length=128, verbose_name=b'Ticket owner'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='ticket_status',
            field=models.CharField(blank=True, choices=[(b'', b'All'), (b'Open', b'Open'), (b'Closed', b'Closed'), (b'Hold', b'Hold')], default=b'All', max_length=64, verbose_name=b'Ticket status'),
        ),
    ]