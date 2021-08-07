# 会员信息管理的视图文件
from django.shortcuts import render
from django.core.paginator import Paginator
from myadmin.models import Member
from datetime import datetime

# Create your views here.

def index(request,pindex=1):
    """浏览信息"""
    smod=Member.objects
    slist=smod.filter(status__lt=9) #lte表示小于等于9，lt表示小于9,实现数据假删除
    #获取并判断搜索条件
    mywhere=[] #维持搜索条件
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
    context={"memberlist":slist2,"pindex":pindex,"plist":plist,"maxpages":maxpages,"mywhere":mywhere}
    return render(request,"myadmin/member/index.html",context)


def delete(request,mid=0):
    """执行信息删除"""
    try:
        ob = Member.objects.get(id=mid)
        ob.status = 9
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {"info": "删除成功!"}
    except Exception as err:
        print(err)
        context = {"info": "删除失败!"}
    return render(request, "myadmin/info.html", context)

