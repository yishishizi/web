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
#后台管理子路由文件
from django.contrib import admin
from django.urls import path
from myadmin.views import index,user,shop,category,product,member

urlpatterns = [
    #path('admin/', admin.site.urls),
    #后台首页
    path('',index.index,name='myadmin_index'),

    #后台管理员登录、退出路由
    path('login',index.login,name="myadmin_login"),#加载登录表单
    path('dologin',index.dologin,name="myadmin_dologin"),#执行登录
    path('logout',index.logout,name="myadmin_logout"),#退出
    path('verify',index.verify,name="myadmin_verify"),#输出验证码

    #员工信息管理路由
    path('user/<int:pindex>',user.index,name='myadmin_user_index'), #浏览
    path('user/add',user.add,name='myadmin_user_add'), #添加表单
    path('user/insert',user.insert,name='myadmin_user_insert'), #执行添加
    path('user/resetcode', user.resetcode, name='myadmin_user_resetcode'),  # 执行添加
    path('user/del/<int:uid>',user.delete,name='myadmin_user_delete'), #执行删除
    path('user/edit/<int:uid>',user.edit,name='myadmin_user_edit'), #加载编辑表单
    path('user/update/<int:uid>',user.update,name='myadmin_user_update'), #执行编辑

    #店铺信息路由配置
    path('shop/<int:pindex>', shop.index, name='myadmin_shop_index'),  # 浏览
    path('shop/add', shop.add, name='myadmin_shop_add'),  # 添加表单
    path('shop/insert', shop.insert, name='myadmin_shop_insert'),  # 执行添加
    path('shop/del/<int:sid>', shop.delete, name='myadmin_shop_delete'),  # 执行删除
    path('shop/edit/<int:sid>', shop.edit, name='myadmin_shop_edit'),  # 加载编辑表单
    path('shop/update/<int:sid>', shop.update, name='myadmin_shop_update'),  # 执行编辑

    #菜品类别信息路由配置
    path('category/<int:pindex>', category.index, name='myadmin_category_index'),  # 浏览
    path('category/load/<int:sid>', category.loadCategory, name="myadmin_category_load"),
    path('category/add', category.add, name='myadmin_category_add'),  # 添加表单
    path('category/insert', category.insert, name='myadmin_category_insert'),  # 执行添加
    path('category/del/<int:cid>', category.delete, name='myadmin_category_delete'),  # 执行删除
    path('category/edit/<int:cid>', category.edit, name='myadmin_category_edit'),  # 加载编辑表单
    path('category/update/<int:cid>', category.update, name='myadmin_category_update'),  # 执行编辑
 
    # 菜品信息路由配置
    path('product/<int:pindex>', product.index, name='myadmin_product_index'),  # 浏览
    path('product/add', product.add, name='myadmin_product_add'),  # 添加表单
    path('product/insert', product.insert, name='myadmin_product_insert'),  # 执行添加
    path('product/del/<int:pid>', product.delete, name='myadmin_product_delete'),  # 执行删除
    path('product/edit/<int:pid>', product.edit, name='myadmin_product_edit'),  # 加载编辑表单
    path('product/update/<int:pid>', product.update, name='myadmin_product_update'),  # 执行编辑

    # 会员信息路由配置
    path('member/<int:pindex>', member.index, name='myadmin_member_index'),  # 浏览
    path('member/del/<int:mid>', member.delete, name='myadmin_member_delete'),  # 执行删除
]
