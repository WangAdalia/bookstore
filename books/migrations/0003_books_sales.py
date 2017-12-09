# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_auto_20171207_0319'),
    ]

    operations = [
        migrations.AddField(
            model_name='books',
            name='sales',
            field=models.IntegerField(verbose_name='商品销量', default=0),
        ),
    ]
