# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Books',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('is_delete', models.BooleanField(default=False, verbose_name='逻辑删除')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(verbose_name='更新时间', auto_now=True)),
                ('title', models.CharField(verbose_name='书籍名称', max_length=50)),
                ('desc', models.CharField(verbose_name='书籍简介', max_length=200)),
                ('price', models.IntegerField(default=0, verbose_name='书籍价格')),
                ('detail', models.CharField(verbose_name='书籍详情', max_length=500)),
                ('unit', models.CharField(verbose_name='书籍单位', max_length=5)),
                ('sales', models.IntegerField(default=0, verbose_name='商品销量')),
                ('type_id', models.SmallIntegerField(default=1, choices=[(1, 'python'), (2, 'Javascript'), (3, '数据结构与算法'), (4, '机器学习'), (5, '操作系统'), (6, '数据库')], verbose_name='书籍类型')),
                ('details', tinymce.models.HTMLField(default='')),
                ('image', models.ImageField(default='', upload_to='books', verbose_name='商品图片')),
                ('status', models.SmallIntegerField(default=1, choices=[(0, '下线'), (1, '上线')], verbose_name='商品状态')),
            ],
            options={
                'db_table': 's_book_info',
            },
        ),
    ]
