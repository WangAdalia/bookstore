from django.conf.urls import url
from cart import views
urlpatterns = [
    url(r'^add/$',views.cart_add,name='add'),
    url(r'^count/$',views.cart_count,name='count'),
    url(r'^$',views.cart_show,name='show'),#显示用户的购物车页面
    url(r'^del/$', views.cart_del, name='delete'), # 购物车商品记录删除
    url(r'^update/$', views.cart_update, name='update'), # 更新购物车商品数目
]