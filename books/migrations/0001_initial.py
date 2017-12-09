# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Books',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('is_delete', models.BooleanField(verbose_name='逻辑删除', default=False)),
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('update_time', models.DateTimeField(verbose_name='更新时间', auto_now=True)),
                ('title', models.CharField(verbose_name='书籍名称', max_length=50)),
                ('desc', models.CharField(verbose_name='书籍简介', max_length=200)),
                ('price', models.IntegerField(verbose_name='书籍价格', default=0)),
                ('detail', models.CharField(verbose_name='书籍详情', max_length=500)),
                ('unit', models.CharField(verbose_name='书籍单位', max_length=5)),
                ('type_id', models.SmallIntegerField(choices=[(1, 'python'), (2, 'Javascript'), (3, '数据结构与算法'), (4, '机器学习'), (5, '操作系统'), (6, '数据库')], verbose_name='书籍类型', default=1)),
                ('status', models.SmallIntegerField(choices=[(0, '下线'), (1, '上线')], verbose_name='商品状态', default=1)),
            ],
            options={
                'db_table': 's_book_info',
            },
        ),
    ]
