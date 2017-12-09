from django.shortcuts import render,redirect
from django.core.urlresolvers import reverse
import re
import json
from users.models import Passport,Address
from django.http import JsonResponse
from utils.decorators import login_required

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
    print(username,'------')
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
            request.session['remember'] = remember
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