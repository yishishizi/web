# 购物车信息管理视图文件
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
import hashlib,random
from PIL import Image, ImageDraw, ImageFont
from myadmin.models import User,Shop,category,Product

def add(request):
    '''添加购物车操作'''
    #尝试从session中获取名为cartlist的购物车信息，若没有返回{}
    cartlist=request.session.get('cartlist',{})
    print(cartlist)
    # 获取要购买的菜品信息
    pid = request.GET.get('pid',None)
    # print(type(pid)) #str类型
    if pid is not None:
        product=Product.objects.get(id=pid).toDict()
        product['num']=1 #初始化当前菜品的购买量
        print(product)
        #判断当前购物车中是否存在要放进购物车中的菜品
        if pid in cartlist:
            if cartlist[pid]['num'] < 0:
                cartlist[pid]['num'] = 0
            cartlist[pid]['num']+=product['num'] #增加购买量
        else:
            cartlist[pid]=product #放进购物车
        #将cartlist放入购物车
        request.session['cartlist']  = cartlist
    a = request.session.get('cartlist',{})
    if a is None:
        a['cartindex'] = 0 # 表示购物车为空
    else:
        a['cartindex'] = 1 # 表示购物车不为空
    # print(cartlist)
    # 响应json格式的购物车数据
    return JsonResponse({"cartlist":cartlist})

def cartinfo(request):
    a = request.session.get('cartlist', {})
    if a is None:
        context = {"info": "购物车为空"}
    return render(request, "mobile/info.html", context)

def reducecart(request):
    cartlist = request.session.get('cartlist', {})
    pid = request.GET.get('pid', None)
    if pid is not None:
        product=Product.objects.get(id=pid).toDict()
        product['num']=1 #初始化当前菜品的购买量
        if pid in cartlist:
            cartlist[pid]['num'] -= product['num']  # 增加购买量
            if cartlist[pid]['num'] < 0:
                cartlist[pid]['num'] = 0
        else:
            cartlist[pid] = product  # 放进购物车
        # 将cartlist放入购物车
        request.session['cartlist'] = cartlist
    # print(cartlist)
    # 响应json格式的购物车数据
    return JsonResponse({"cartlist": cartlist})

def delete(request):
    '''删除购物车中商品操作'''
    pid = request.GET.get('pid', None)
    cartlist = request.session.get('cartlist', {})
    del cartlist[pid]
    request.session['cartlist'] = cartlist
    return JsonResponse({"cartlist":cartlist})

def clear(request):
    '''清空购物车操作'''
    request.session['cartlist'] = {}
    return JsonResponse({"cartlist":{}})

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
    return JsonResponse({"cartlist":cartlist})
