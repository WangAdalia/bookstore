from django.shortcuts import render,redirect
from django.core.urlresolvers import reverse
import re
from bookstore import settings
from django.core.mail import send_mail
from users.models import Passport,Address
from django.http import JsonResponse,HttpResponse
from utils.decorators import login_required
from order.models import OrderInfo,OrderGoods
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import random
from PIL import Image,ImageDraw,ImageFont
import io

# Create your views here.
def register(request):
    return render(request, 'users/register.html')

def register_handle(request):
    '''进行用户注册处理'''
    #接收数据
    username = request.POST.get('user_name')
    password = request.POST.get('pwd')
    email = request.POST.get('email')
    print('email: ', email)
    if not all([username,password,email]):
        return render(request, 'users/register.html', {'errmsg': '参数不能为空！！'})
    if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$',email):
        return render(request, 'users/register.html', {'errmsg': '邮箱不合法！！！'})

    p = Passport.objects.check_passport(username=username)
    if p:
        return render(request,'users/register.html',{'errmsg':'用户名已存在！'})
    passport = Passport.objects.add_one_passport(username=username,password=password,email=email)
    #生成激活的token itsdangerous
    serializer = Serializer(settings.SECRET_KEY,3600)
    token = serializer.dumps({'confirm':passport.id})
    token = token.decode()
    print(token)
    #给用户的邮箱激活邮件
    try:
        send_mail('尚硅谷书城用户激活', '', settings.EMAIL_FROM, [email], html_message='<a href="http://127.0.0.1:8000/user/active/%s/">http://127.0.0.1:8000/user/active/</a>' % token)
        return redirect(reverse('books:index'))
    except Exception as e:
        print(e)
        return None


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
    verifycode = request.POST.get('verifycode')
    #数据校验
    if not all([username,password,remember,verifycode]):

         return JsonResponse({'res':2})
    if verifycode.upper() != request.session['verifycode']:
        return JsonResponse({'res':2})
    #处理数据：
    passport = Passport.objects.get_one_passport(username=username,password=password)
    if passport:
        #next_url = request.session.get('url_path',reverse('books:index'))
        next_url = reverse('books:index')
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
        addr = Address.objects.get_default_address(passport_id=passport_id)
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
def verifycode(request):
    #引入绘图模块
    bgcolor = (random.randrange(20,100),random.randrange(20,100),255)
    width = 100
    height = 25
    #创建画面对象
    im = Image.new('RGB',(width,height),bgcolor)
    #创建画笔对象
    draw = ImageDraw.Draw(im)
    #调用画笔的point()函数绘制噪点
    for i in range(0,100):
        xy = (random.randrange(0,width),random.randrange(0,height))
        fill = (random.randrange(0,255),255,random.randrange(0,255))
        draw.point(xy,fill=fill)
        #定义验证码的备选值
        str1 = 'ABCD123EFGIJK456LMNOPQRS789TUVWXYZ0'
        #随机选取4个值作为验证码
        rand_str = ''
        for i in range(0,4):
            rand_str += str1[random.randrange(0,len(str1))]
        #构造字体对象
        font = ImageFont.truetype('/usr/share/fonts/truetype/fonts-japanese-gothic.ttf',15)
        #构造字体颜色
        fontcolor = (255,random.randrange(0,255),random.randrange(0,255))
        #绘制4个字
        draw.text((5,2),rand_str[0],font=font,fill=fontcolor)
        draw.text((25,2),rand_str[1],font=font,fill=fontcolor)
        draw.text((50,2),rand_str[2],font=font,fill=fontcolor)
        draw.text((75,2),rand_str[3],font=font,fill=fontcolor)
        #释放笔画
        del draw
        #存入session,用于做进一步验证
        request.session['verifycode'] = rand_str
        #存入文件操作
        buf = io.BytesIO()
        #将图片保存在内存中，文件类型为png
        im.save(buf,'png')
        #将内存中的图片数据返回给客户端,MIME类型为图片png
        return HttpResponse(buf.getvalue(),'image/png')





