# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-10 09:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enable_api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='device_detail_feed',
            name='is_prefix',
            field=models.CharField(default='', max_length=255),
        ),
    ]
