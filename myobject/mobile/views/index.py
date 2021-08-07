from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from myadmin.models import Member,Shop,category,Product,Payment,Order,OrderDetail
import time
from datetime import datetime
# Create your views here.

def index(request):
    '''移动端首页'''
    # 获取并判断当前店铺信息
    shopinfo=request.session.get('shopinfo',None)
    # print(shopinfo)
    if shopinfo is None:
        return redirect(reverse("mobile_shop"))
    # 获取当前店铺下的菜品类别和菜品信息
    clist=category.objects.filter(shop_id=request.session['shopinfo']['id'],status=1)
    productlist = dict()
    for vo in clist:
        # print(vo.toDict())
        plist=Product.objects.filter(category_id=vo.id,shop_id=request.session['shopinfo']['id'],status=1) #vo.id为菜品类别id
        # print(plist[0].toDict())
        productlist[vo.id] = plist
        # print(productlist)
    context={'categorylist':clist,'productlist':productlist.items(),'cid':clist[0]}
    # for k,v in productlist.items():
    #     print(k)
    #     for p in v:
    #         print(p.toDict())

    return render(request,"mobile/index.html",context)

def register(request):
    '''移动端会员注册/登录表单'''
    return render(request,"mobile/register.html")


def doregister(request):
    '''执行会员注册登录'''
    # 模拟短信验证
    verifycode = "1234" #request.session['veriftcode']
    if verifycode != request.POST['code']:
        context = {"info": "验证码错误"}
        return render(request, "mobile/register.html", context)
    try:
        # 根据手机号码获取当前会员信息
        mmod = Member.objects.get(mobile=request.POST['mobile'])
        if mmod.status == 1:
            request.session['mobileuser'] = mmod.toDict()
            return redirect(reverse("mobile_index"))
        else:
            context={"info": "此账号异常！"}
            return render(request, "mobile/register.html", context)
    except Exception as err:
        print(err)
        #执行当前会员注册
        return render(request,"mobile/addmember.html")

def doaddmember(request):
    try:
        print("开始注册")
        verifycode = "1234"  # request.session['veriftcode']
        print(bool(verifycode==request.POST['code']))
        if verifycode == request.POST['code']:
            myfile = request.FILES.get("pic", None)
            if not myfile:
                return HttpResponse("没有上传头像")
            pic = str(time.time()) + "." + myfile.name.split('.').pop()
            destination = open("./static/uploads/member/" + pic, "wb+")
            for chunk in myfile.chunks():  # 分块写入文件
                destination.write(chunk)
            destination.close()
            m = Member()
            m.nickname = request.POST.get('nickname')
            m.mobile = request.POST.get('mobile')
            m.avatar = pic
            m.status = 1
            m.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            m.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            m.save()
            context = {"info": "注册成功！"}
            return render(request, "mobile/register.html",context)
    except Exception as err:
        print(err)
        context = {"info": "注册失败！"}
        return render(request, "mobile/register.html", context)


def shop(request):
    '''移动端选择店铺'''
    context = {"shoplist":Shop.objects.filter(status=1)}
    return render(request,"mobile/shop.html",context)

def selectshop(request):
    '''移动端首页'''
    # 获取选择的店铺信息，并放置到session中，跳转到店铺首页
    sid = request.GET['sid']
    ob = Shop.objects.get(id=sid)
    request.session['shopinfo'] = ob.toDict()
    request.session['cartlist'] = {} # 清空购物车
    return redirect(reverse('mobile_index'))

def addOrders(request):
    '''移动端下单页面'''
    cartlist = request.session.get('cartlist',{})
    print(cartlist)
    total_money = 0 #初始化一个总金额
    #遍历购物车的菜品，并计算总金额
    for v in cartlist.values():
        total_money+=v['num']*v['price']
    request.session['total_money'] = total_money
    return render(request,"mobile/addorders.html")

def doaddorders(request):
    try:
        #执行订单信息的添加
        od = Order()
        od.shop_id = request.session['shopinfo']['id'] #获取当前店铺信息，在执行登录时存入了session
        od.member_id = request.session['mobileuser']['id']
        od.user_id = 0  #获取用户信息，在执行登录时存入了session
        od.money = request.session['total_money'] #获取订单总金额
        od.status = 1  # 订单状态:1过行中/2无效/3已完成
        od.payment_status = 2 #支付状态:1未支付/2已支付/3已退款
        od.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        od.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        od.save()

        #执行支付信息添加
        op = Payment()
        op.order_id = od.id #订单id号
        op.member_id = request.session['mobileuser']['id']
        op.type = 2
        op.bank = request.GET.get('bank',1)
        op.money = request.session['total_money']
        op.status = 2  # 订单状态:1过行中/2无效/3已完成
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

        del request.session['cartlist']
        del request.session['total_money']
    except Exception as err:
        print(err)
    return render(request, "mobile/orderinfo.html", {"order": od})