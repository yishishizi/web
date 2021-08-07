"""myobject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
#会员移动端子路由文件
from django.contrib import admin
from django.urls import path
from mobile.views import index,member,cart

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('',index.index,name='mobile_index'),#移动端首页

    #会员注册/登录
    path('register',index.register,name='mobile_register'),#移动端会员注册/登录表单页
    path('doregister',index.doregister,name='mobile_doregister'),#移动端执行注册/登录
    path('doaddmember',index.doaddmember,name="mobile_doaddmember"),

    #店铺选择
    path('shop',index.shop,name='mobile_shop'),# 移动端店铺选择页
    path('shop/select', index.selectshop, name='mobile_selectshop'),  # 执行移动端店铺选择

    # 购物车信息管理路由
    path('cart/add', cart.add, name='mobile_cart_add'),  # 购物车添加
    path('cart/reducecart', cart.reducecart, name='mobile_cart_reducecart'),  # 购物车删除一次
    path('cart/delete', cart.delete, name='mobile_cart_delete'),  # 购物车删除
    path('cart/clear', cart.clear, name='mobile_cart_clear'),  # 购物车清空
    path('cart/change', cart.change, name='mobile_cart_change'),  # 购物车更改
    path('cart/cartinfo', cart.cartinfo, name='mobile_cart_cartinfo'),  # 购物车更改

    #订单处理
    path('orders/add',index.addOrders,name='mobile_addorders'),# 加载移动端订单页
    path('orders/doadd',index.doaddorders,name='mobile_doaddorders'),# 执行移动端订单添加

    #会员中心
    path('member', member.index, name='mobile_member_index'),  # 会员中心首页
    path('member/orders', member.orders, name='mobile_member_orders'),  # 加载会员中心订单页
    path('member/detail', member.detail, name='mobile_member_detail'),  # 加载会议中心订单详情页
    path('member/logout', member.logout, name='mobile_member_logout'),  # 执行会员退出



]