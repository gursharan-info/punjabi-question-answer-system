# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-09 17:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0006_auto_20160309_2235'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dictionary',
            name='Word',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='word'),
        ),
    ]