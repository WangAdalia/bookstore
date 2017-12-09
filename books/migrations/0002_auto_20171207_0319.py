# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='books',
            name='details',
            field=tinymce.models.HTMLField(default=''),
        ),
        migrations.AddField(
            model_name='books',
            name='image',
            field=models.ImageField(default='', upload_to='books', verbose_name='商品图片'),
        ),
    ]
