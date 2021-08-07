# 订单信息管理视图文件
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
import hashlib,random
from PIL import Image, ImageDraw, ImageFont
from myadmin.models import User,Shop,category,Product,Order,OrderDetail,Payment,Member
from datetime import datetime
from django.core.paginator import Paginator

def index(request,pindex=1):
    '''浏览订单信息'''
    omod = Order.objects
    sid=request.session['shopinfo']['id'] # 获取当前店铺id号
    slist = omod.filter(shop_id=sid)  # lte表示小于等于9，lt表示小于9,实现数据假删除
    # 获取并判断搜索条件
    mywhere = []  # 维持搜索条件
    status = request.GET.get("status", "")
    if status != "":
        slist = slist.filter(status=status)
        mywhere.append("status=" + status)

    slist = slist.order_by('-id')  # 对id进行排序
    # 执行分页处理
    pindex = int(pindex)
    page = Paginator(slist, 10)  # 以每页10条数据分页
    maxpages = page.num_pages  # 获取最大页数
    # 判断当前页是否越界
    if pindex > maxpages:
        pindex = maxpages
    if pindex < 1:
        pindex = 1
    slist2 = page.page(pindex)  # 获取当前页数据
    plist = page.page_range  # 获取页面列表信息))
    for vo in slist2:
        if vo.user_id == 0: # 如果是移动端点餐，则无操作员
            vo.nickname = "无"
        else:
            user = User.objects.get(id=vo.user_id)
            vo.nickname = user.nickname

        if vo.user_id == 0: # 如果是移动端点餐，则无操作员
            vo.membername = "大堂顾客"
        else:
            member = Member.objects.only('mobile').get(id=vo.member_id)
            vo.membername = member.mobile

    context = {"orderslist": slist2, "pindex": pindex, "plist": plist, "maxpages": maxpages, "mywhere": mywhere}
    return render(request, "web/list.html", context)

def insert(request):
    '''执行订单的添加'''
    try:
        #执行订单信息的添加
        od = Order()
        od.shop_id = request.session['shopinfo']['id'] #获取当前店铺信息，在执行登录时存入了session
        od.member_id = 0
        od.user_id = request.session['webuser']['id'] #获取用户信息，在执行登录时存入了session
        od.money = request.session['total_money'] #获取订单总金额
        od.status = 1  # 订单状态:1过行中/2无效/3已完成
        od.payment_status = 2 #支付状态:1未支付/2已支付/3已退款
        od.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        od.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        od.save()

        #执行支付信息添加
        op = Payment()
        op.order_id = od.id #订单id号
        op.member_id = 0
        op.type = 2
        op.bank = request.GET.get('bank',3)
        op.money = request.session['total_money']
        op.status = 1  # 订单状态:1过行中/2无效/3已完成
        op.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        op.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        op.save()

        # 执行订单详情的添加
        cartlist = request.session.get('cartlist',{}) #获取购物车信息
        # 遍历购物车中的菜品，并添加到订单详情中
        for item in cartlist.values():
            ov = OrderDetail()
            ov.order_id = od.id
            ov.product_id = item['id']
            ov.product_name = item['name']
            ov.price = item['price']
            ov.quantity = item['num']
            ov.status = 1
            ov.save()

        del request.session['cartlist'] #订单添加完之后清楚购物车信息
        del request.session['total_money']
        return HttpResponse("Y")
    except Exception as err:
        print(err)
        return HttpResponse("N")

def detail(request):
    '''加载订单信息'''
    oid = request.GET.get("oid",0)
    dlist = OrderDetail.objects.filter(order_id=oid)
    context = {"detaillist":dlist}
    return render(request, "web/detail.html", context)


def status(request):
    '''修改订单信息'''
    try:
        oid = request.GET.get("oid",0)
        ob = Order.objects.get(id=oid)
        ob.status = request.GET.get("status")
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        return HttpResponse("Y")
    except Exception as err:
        print(err)
        return HttpResponse("N")