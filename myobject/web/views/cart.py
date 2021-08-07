# 购物车信息管理视图文件
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
import hashlib,random
from PIL import Image, ImageDraw, ImageFont
from myadmin.models import User,Shop,category,Product

def add(request,pid):
    '''添加购物车操作'''
    #从session中获取当前店铺中所有的菜品信息，并从中获取要放入购物车的菜品
    # print(request.session['productlist'])
    # p=request.session['productlist']
    # print(p)
    # print('---------------')
    # print(p[str(pid)])
    pid=str(pid)
    product=request.session['productlist'][pid]
    product['num']=1 #初始化当前菜品的购买量
    #尝试从session中获取名为cartlist的购物车信息，若没有返回{}
    cartlist=request.session.get('cartlist',{})
    #判断当前购物车中是否存在要放进购物车中的菜品
    if pid in cartlist:
        cartlist[pid]['num']+=product['num'] #增加购买量
    else:
        cartlist[pid]=product #放进购物车
    #将cartlist放入购物车
    request.session['cartli st']  = cartlist
    # print(cartlist)
    return redirect(reverse('web_index'))

def delete(request,pid):
    '''删除购物车中商品操作'''
    pid=str(pid)
    cartlist = request.session.get('cartlist', {})
    del cartlist[pid]
    request.session['cartlist'] = cartlist
    return redirect(reverse('web_index'))

def clear(request):
    '''清空购物车操作'''
    request.session['cartlist'] = {}
    return redirect(reverse('web_index'))

def change(request):
    '''更改购物车操作'''
    cartlist = request.session.get('cartlist', {})
    pid = request.GET.get("pid",0) # 获取要修改的菜品id
    m = int(request.GET.get("num",1)) #获取要修改的数量
    if m < 1:
        m = 1
    pid=str(pid)
    cartlist[pid]['num'] = m
    request.session['cartlist'] = cartlist
    return redirect(reverse('web_index'))
