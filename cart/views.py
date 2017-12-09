from django.shortcuts import render
from django.http import JsonResponse
from books.models import Books
from utils.decorators import login_required
from django_redis import get_redis_connection
# Create your views here.

def cart_add(request):
    '''购物车中添加数据'''
    #判断用户是否登录
    if not request.session.has_key('islogin'):
        return JsonResponse({'res':0,'errmsg':'请先登录'})
    #接收数据
    books_id = request.POST.get('books_id')
    books_count = request.POST.get('books_count')
    #进行数据校验
    if not all([bool,books_count]):
        return JsonResponse({'res':1,'errmsg':'数据不完整'})
    books = Books.objects.get_books_id(books_id=books_id)
    if books is None:
        #商品不存在
        return JsonResponse({'res':2,'errmsg':'商品不存在'})
    try:
        count = int(books_count)
    except Exception as e:
        #商品数量不合法，数量必须为数字
        return JsonResponse({'res':3,'errmsg':'商品数量必须为数字'})

    #添加商品到购物车中
    conn = get_redis_connection('default')
    cart_key = 'cart_%d'%request.session.get('passport_id')
    res = conn.hget(cart_key,books_id)
    if res in None:
        #如果用户的购物车没有该商品,就添加
        res = count
    else:
        #如果用户的购物车中已添加,则累计添加
        res = int(res) + count
    #判断商品的库存
    if res > books.stock:
        #库存不足
        return JsonResponse({'res':4,'errmsg':'商品库存不足'})
    else:
        conn.hset(cart_key,books_id,res)
    #返回结果
    return JsonResponse({'res':5})
def cart_count(request):
    '''获取用户购物车中商品的数目'''
    #判断用户是否登录
    if not request.session.has_key('islogin'):
        return JsonResponse({'res':0})
    #计算用户购物车的数量
    conn = get_redis_connection('default')
    cart_key = 'cart_%d'%request.session.get('passport_id')
    res = 0
    res_list = conn.hvals(cart_key)
    for i in res_list:
        res += int(i)
    #返回结果
    return JsonResponse({'res':res})


