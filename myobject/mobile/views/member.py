from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from myadmin.models import User,Shop,category,Product,Order,OrderDetail,Payment,Member
# Create your views here.

def index(request):
    '''个人中心首页'''
    return render(request,"mobile/member.html")

def orders(request):
    '''个人中心浏览订单'''
    omod = Order.objects
    mid = request.session['mobileuser']['id']  # 获取当前会员id号
    slist = omod.filter(member_id=mid)  # lte表示小于等于9，lt表示小于9,实现数据假删除
    # 获取并判断搜索条件

    status = request.GET.get("status", "")
    if status != "":
        slist = slist.filter(status=status)
    list2 = slist.order_by('-id')  # 对id进行降序排序
    for vo in list2:
        print('--------------------------------------------------------')
        print(vo.toDict())
        plist=OrderDetail.objects.filter(order_id=vo.id)[:4] #获取头4条
        vo.plist = plist
        print('--------------------------------------------------------')
        print(vo.toDict())
    context = {"orderslist": list2}
    return render(request,"mobile/member_orders.html",context)

def detail(request):
    '''个人中心中的订单详情'''
    pid = request.GET.get("pid",0)
    # 获取当前订单
    order = Order.objects.get(id=pid)
    # 获取订单详情
    plist = OrderDetail.objects.filter(order_id=order.id)
    order.list = plist
    #  获取店铺名称
    shop = Shop.objects.only("name").get(id=order.shop_id)
    order.name = shop.name
    return render(request,"mobile/member_detail.html",{"order":order})

def logout(request):
    '''会员退出'''
    del request.session['mobileuser']
    del request.session['shopinfo']
    return render(request,"mobile/register.html")
