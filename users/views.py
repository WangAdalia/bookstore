from django.shortcuts import render,redirect
from django.core.urlresolvers import reverse
import re
import json
from users.models import Passport,Address
from django.http import JsonResponse
from utils.decorators import login_required
from order.models import OrderInfo,OrderGoods

# Create your views here.
def register(request):
    return render(request, 'users/register.html')

def register_handle(request):
    '''进行用户注册处理'''
    #接收数据
    username = request.POST.get('user_name')
    password = request.POST.get('pwd')
    email = request.POST.get('email')
    if not all([username,password,email]):
        return render(request, 'users/register.html', {'errmsg': '参数不能为空！！'})
    if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$',email):
        return render(request, 'users/register.html', {'errmsg': '邮箱不合法！！！'})

    Passport.objects.add_one_passport(username=username, password=password, email=email)
    #passport = Passport.objects.add_one_passport(username=username,password=password,email=email)
    return redirect(reverse('user:login'))

def login(request):
    context = {
        'username':'',
        'password':''
    }
    return render(request,'users/login.html',context)

def login_check(request):
    print('request: ', request.body)

    # data = json.loads(request.body.decode('utf-8'))
    # print(data)
    '''进行用户登录校验'''
    #获取数据
    username = request.POST.get('username')
    password = request.POST.get('password')
    remember = request.POST.get('remember')
    #数据校验
    if not all([username,password]):

         return JsonResponse({'res':2})
    #处理数据：
    passport = Passport.objects.get_one_passport(username=username,password=password)
    if passport:
        next_url = request.session.get('url_path',reverse('books:index'))
        jres = JsonResponse({'res':1,'next_url':next_url})
        if remember =='true':
            #记住用户名
            jres.set_cookie('username',username,max_age=7*24*3600)
        else:
            #不记住用户名
            jres.delete_cookie('username')
            #记住用户登录状态
            request.session['islogin'] = True
            request.session['username'] = username
            request.session['passport_id'] = passport.id
        return jres
    else:
        return JsonResponse({'res':0})

def logout(request):
    request.session.flush()
    return redirect(reverse('books:index'))
@login_required
def user(request):
    '''用户中心信息页'''
    passport_id = request.session.get('passport_id')
    addr = Address.objects.get_default_address(passport_id=passport_id)
    books_li = []
    context = {
        'addr':addr,
        'page':'user',
        'books_li':books_li
    }
    return render(request,'users/user_center_info.html',context)

@login_required
def address(request):
    '''用户中心,地址页'''
    #获取登录用户的id
    passport_id = request.session.get('passport_id')
    if request.method =='GET':
        #显示地址页面
        #查询用户的默认地址
        addr = Address.objects.get_default_address(passport_is=passport_id)
        return render(request,'users/user_center_site.html',{'addr':addr,'page':'address'})
    else:
        #添加收货地址
        #1.接收数据
        recipient_name = request.POST.get('username')
        recipient_addr = request.POST.get('addr')
        zip_code = request.POST.get('zip_code')
        recipient_phone = request.POST.get('phone')
        #2.进行校验
        if not all([recipient_name,recipient_addr,zip_code,recipient_phone]):
            return render(request,'users/user_center_site.html',{'errmsg':'参数不必为空!'})
        #添加收货地址
        Address.objects.add_one_address(passport_id=passport_id,
                                        recipient_name=recipient_name,
                                        recipient_addr=recipient_addr,
                                        zip_code=zip_code,
                                        recipient_phone=recipient_phone)
        #返回应答
        return redirect(reverse('user:address'))
@login_required
def order(request):
    '''用户中心-订单页'''
    #查询用户的订单信息
    passport_id = request.session.get('passport_id')
    #获取订单信息
    order_li = OrderInfo.objects.filter(passport_id=passport_id)
    #遍历获取订单的商品信息
    for order in order_li:
        #根据订单id查询订单商品信息
        order_id =  order.order_id
        order_books_li = OrderGoods.objects.filter(order_id=order_id)
        #计算商品的小计
        #order_books -->OrderBooks实例对象
        for order_books in order_books_li:
            count = order_books.count
            price = order_books.count
            amount = count*price
            #保存订单中每一个商品的小计
            order_books.amount = amount
            #给order对象动态添加一个属性
        order.order_books_li = order_books_li
        context = {
            'order_li':order_li,
            'page':'order'
            }
    return render(request,'users/user_center_order.html',context)
