# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_books_sales'),
        ('users', '0002_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderGoods',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('is_delete', models.BooleanField(verbose_name='删除标记', default=False)),
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('count', models.IntegerField(verbose_name='商品数量', default=1)),
                ('price', models.DecimalField(max_digits=10, decimal_places=2, verbose_name='商品价格')),
                ('books', models.ForeignKey(verbose_name='订单商品', to='books.Books')),
            ],
            options={
                'db_table': 's_order_books',
            },
        ),
        migrations.CreateModel(
            name='OrderInfo',
            fields=[
                ('is_delete', models.BooleanField(verbose_name='删除标记', default=False)),
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('order_id', models.CharField(primary_key=True, serialize=False, verbose_name='订单编号', max_length=64)),
                ('total_count', models.IntegerField(verbose_name='商品总数', default=1)),
                ('total_price', models.DecimalField(max_digits=10, decimal_places=2, verbose_name='商品总价')),
                ('transit_price', models.DecimalField(max_digits=10, decimal_places=2, verbose_name='订单运费')),
                ('pay_method', models.SmallIntegerField(verbose_name='支付方式', default=1, choices=[(1, '货到付款'), (2, '微信支付'), (3, '支付宝'), (4, '银联支付')])),
                ('status', models.SmallIntegerField(verbose_name='订单状态', default=1, choices=[(1, '待支付'), (2, '待发货'), (3, '待收货'), (4, '已完成')])),
                ('trade_id', models.CharField(blank=True, null=True, verbose_name='支付编号', unique=True, max_length=100)),
                ('addr', models.ForeignKey(verbose_name='收货地址', to='users.Address')),
                ('passport', models.ForeignKey(verbose_name='下单账户', to='users.Passport')),
            ],
            options={
                'db_table': 's_order_info',
            },
        ),
        migrations.AddField(
            model_name='ordergoods',
            name='order',
            field=models.ForeignKey(verbose_name='所属订单', to='order.OrderInfo'),
        ),
    ]
