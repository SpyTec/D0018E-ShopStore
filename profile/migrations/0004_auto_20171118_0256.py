# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-18 01:56
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0003_auto_20171118_0253'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='post_city',
            new_name='city',
        ),
    ]
