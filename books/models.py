from django.db import models
from books.enums import *
from db.base_model import BaseModel
from tinymce.models import HTMLField


class BooksManager(models.Manager):
    '''商品模型管理器类'''
    # sort='new' 按照创建时间进行排序
    # sort='hot' 按照商品销量进行排序
    # sort='price' 按照商品的价格进行排序
    # sort= 按照默认顺序排序
    def get_books_by_type(self, type_id, limit=None, sort='default'):
        '''根据商品类型id查询商品信息'''
        if sort == 'new':
            order_by = ('-create_time',)
        elif sort == 'hot':
            order_by = ('-sales', )
        elif sort == 'price':
            order_by = ('price', )
        else:
            order_by = ('-pk', ) # 按照primary key降序排列。

        # 查询数据
        books_li = self.filter(type_id=type_id).order_by(*order_by)

        # 查询结果集的限制
        if limit:
            books_li = books_li[:limit]
        return books_li

    def get_books_by_id(self, books_id):
        '''根据商品的id获取商品信息'''
        try:
            books = self.get(id=books_id)
        except self.model.DoesNotExist:
            # 不存在商品信息
            books = None
        return books

# Create your models here.
class Books(models.Model):
    is_delete = models.BooleanField(default=False,verbose_name='逻辑删除')
    create_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True,verbose_name='更新时间')
    title = models.CharField(max_length=50,verbose_name='书籍名称')
    desc = models.CharField(max_length=200,verbose_name='书籍简介')
    price = models.IntegerField(default=0,verbose_name='书籍价格')
    detail = models.CharField(max_length=500,verbose_name='书籍详情')
    unit = models.CharField(max_length=5,verbose_name='书籍单位')
    sales = models.IntegerField(default=0, verbose_name='商品销量')
    type_id = models.SmallIntegerField(default=PYTHON,choices=((k,v)for k,v in BOOK_TYPES.items()),verbose_name='书籍类型')
    status = models.SmallIntegerField(default=ONLINE,choices=((k,v)for k,v in STATUSES.items()),verbose_name='商品状态')
    details = HTMLField(default='')
    image = models.ImageField(default='',upload_to='books',verbose_name='商品图片')
    objects = BooksManager()
    class Meta:
        db_table = 's_book_info'