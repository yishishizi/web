from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from myadmin.models import Shop
from datetime import datetime
import hashlib,random
import time

# Create your views here.

def index(request,pindex=1):
    """浏览信息"""
    smod=Shop.objects
    slist=smod.filter(status__lt=9) #lte表示小于等于9，lt表示小于9,实现数据假删除
    #获取并判断搜索条件
    kw=request.GET.get("keyword",None)
    mywhere=[] #维持搜索条件
    if kw :
        slist = slist.filter(name__contains=kw)
        mywhere.append('keyword='+kw)
    status=request.GET.get("status","")
    if status !="":
        slist=slist.filter(status=status)
        mywhere.append("status="+status)

    slist=slist.order_by('id')#对id进行排序
    #执行分页处理
    pindex=int(pindex)
    page = Paginator(slist,5) #以每页五条数据分页
    maxpages = page.num_pages #获取最大页数
    #判断当前页是否越界
    if pindex>maxpages:
        pindex=maxpages
    if pindex<1:
        pindex=1
    slist2=page.page(pindex) #获取当前页数据
    plist=page.page_range #获取页面列表信息
    context={"shoplist":slist2,"pindex":pindex,"plist":plist,"maxpages":maxpages,"mywhere":mywhere}
    return render(request,"myadmin/shop/index.html",context)

def add(request):
    """加载信息添加表单"""
    return render(request,"myadmin/shop/add.html")

def insert(request):
    """执行信息添加"""
    try:
        # 店铺封面图片的上传处理
        myfile = request.FILES.get("cover_pic", None)
        if not myfile:
            return HttpResponse("没有店铺封面上传文件信息")
        cover_pic = str(time.time()) + "." + myfile.name.split('.').pop()
        destination = open("./static/uploads/shop/" + cover_pic, "wb+")
        for chunk in myfile.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()

        # 店铺logo图片的上传处理
        myfile = request.FILES.get("banner_pic", None)
        if not myfile:
            return HttpResponse("没有店铺logo上传文件信息")
        banner_pic = str(time.time()) + "." + myfile.name.split('.').pop()
        destination = open("./static/uploads/shop/" + banner_pic, "wb+")
        for chunk in myfile.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()

        #实例化model，封装信息，并执行添加操作
        ob=Shop()
        ob.name = request.POST.get("name")
        userinfo = Shop.objects.filter(name=ob.name)
        # for s in userinfo:
        #     print(s.name,s.status)
        # print(userinfo)
        if userinfo.exists():
            context = {"info": "店铺名称重复!"}
            return render(request, "myadmin/info.html", context)
        ob.address = request.POST.get("address")
        ob.phone = request.POST.get("phone")
        ob.cover_pic = cover_pic
        ob.banner_pic = banner_pic
        ob.status = 1
        ob.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context={"info":"添加成功!"}
    except Exception as err:
        print(err)
        context={"info":"添加失败!"}
    return render(request,"myadmin/info.html",context)

def delete(request,sid=0):
    """执行信息删除"""
    try:
        ob = Shop.objects.get(id=sid)
        ob.status = 9
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {"info": "删除成功!"}
    except Exception as err:
        print(err)
        context = {"info": "删除失败!"}
    return render(request, "myadmin/info.html", context)

def edit(request,sid=0):
    """加载信息编辑表单"""
    try:
        ob = Shop.objects.get(id=sid)
        ob.save()
        context = {"shop": ob}
        return render(request, "myadmin/shop/edit.html", context)
    except Exception as err:
        print(err)
        context = {"info": "未找到要修改的信息!"}
        return render(request, "myadmin/info.html", context)

def update(request,sid=0):
    """执行信息删除"""
    try:
        ob = Shop.objects.get(id=sid)
        ob.name = request.POST.get("name")
        ob.status = request.POST.get("status")
        ob.address = request.POST.get("address")
        ob.phone = request.POST.get("phone")
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {"info": "修改成功!"}
    except Exception as err:
        print(err)
        context = {"info": "修改失败!"}
    return render(request, "myadmin/info.html", context)