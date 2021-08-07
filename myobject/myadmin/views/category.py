# 菜品类别信息管理的视图文件
from django.shortcuts import render
from django.core.paginator import Paginator
from myadmin.models import category,Shop
from django.db.models import Q #Q专门用来封装或的操作
from datetime import datetime
from django.http import JsonResponse
import hashlib,random
# Create your views here.

def index(request,pindex=1):
    """浏览信息"""
    #浏览信息，浏览的是类变量
    umod=category.objects
    ulist=umod.filter(status__lt=9) #lte表示小于等于9，lt表示小于9,实现数据假删除
    #获取并判断搜索条件
    kw=request.GET.get("keyword",None)
    print(kw)
    mywhere=[] #维持搜索条件
    if kw :
        ulist = ulist.filter(name__contains=kw)
        mywhere.append('keyword='+kw)
    print(list(vo.name for vo in ulist))
    #获取、判断并封装状态status搜索条件

    status=request.GET.get("status","")
    if status !="":
        ulist=ulist.filter(status=status)
        mywhere.append("status="+status)
    #执行分页处理
    ulist = ulist.order_by('id')  # 对id进行排序
    pindex=int(pindex)
    page = Paginator(ulist,10) #以每页10条数据分页
    maxpages = page.num_pages #获取最大页数
    #判断当前页是否越界
    if pindex>maxpages:
        pindex=maxpages
    if pindex<1:
        pindex=1
    ulist2=page.page(pindex) #获取当前页数据
    plist=page.page_range #获取页面列表信息

    #遍历当前菜品分类信息并封装对于的店铺信息
    for vo in ulist2:
        sob = Shop.objects.get(id=vo.shop_id)
        vo.shopname =sob.name

    context={"categorylist":ulist2,"pindex":pindex,"plist":plist,"maxpages":maxpages,"mywhere":mywhere}
    return render(request,"myadmin/category/index.html",context)

def loadCategory(request,sid):
    clist = category.objects.filter(status__lt=9,shop_id=sid).values("id","name")
    #返回QuerySet对象，使用list强转成对应的菜品分类列表信息
    return JsonResponse({'data':list(clist)})

def add(request):
    """加载信息添加表单"""
    #获取当前所有菜品信息
    slist = Shop.objects.values("id","name")
    context = {"shoplist":slist}
    return render(request,"myadmin/category/add.html",context)

def insert(request):
    """执行信息添加"""
    #添加、修改信息，改的是对象中的实例变量
    try:
        ob=category()
        ob.shop_id= request.POST.get("shop_id")
        ob.name = request.POST.get("name")
        userinfo = category.objects.filter(name=ob.name).exclude(shop_id=ob.shop_id)
        #print(userinfo)
        if userinfo.exists():
            context = {"info": "菜品名称重复!"}
            return render(request, "myadmin/info.html", context)
        ob.status = 1
        ob.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context={"info":"添加成功!"}
    except Exception as err:
        print(err)
        context={"info":"添加失败!"}
    return render(request,"myadmin/info.html",context)

def delete(request,cid=0):
    """执行信息删除"""
    try:
        ob = category.objects.get(id=cid)
        ob.status = 9
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {"info": "删除成功!"}
    except Exception as err:
        print(err)
        context = {"info": "删除失败!"}
    return render(request, "myadmin/info.html", context)

def edit(request,cid=0):
    """加载信息编辑表单"""
    try:
        ob = category.objects.get(id=cid)
        ob.save()
        slist = Shop.objects.values("id", "name")
        context = {"category": ob,"shoplist": slist}
        return render(request, "myadmin/category/edit.html", context)
    except Exception as err:
        print(err)
        context = {"info": "未找到要修改的信息!"}
        return render(request, "myadmin/info.html", context)

def update(request,cid=0):
    """执行信息删除"""
    try:
        ob = category.objects.get(id=cid)
        ob.shop_id = request.POST.get("shop_id")
        ob.name = request.POST.get("name")
        ob.status = request.POST.get("status")
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {"info": "修改成功!"}
    except Exception as err:
        print(err)
        context = {"info": "修改失败!"}
    return render(request, "myadmin/info.html", context)

