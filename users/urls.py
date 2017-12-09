from django.conf.urls import url
from users import views

urlpatterns = [
    url(r'^register/',views.register,name='register'),
    url(r'^register_handle/',views.register_handle,name='register_handle'),#用户注册处理
    url(r'^login/',views.login,name='login'),#显示登录页面
    url(r'^login_check/',views.login_check,name='login_check'),
    url(r'^logout/',views.logout,name='logout'),#退出用户登录
    url(r'^$',views.user,name='user'),#用户中心信息页

]
