# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='zip_code',
            field=models.CharField(verbose_name='邮政编码', max_length=7),
        ),
    ]
