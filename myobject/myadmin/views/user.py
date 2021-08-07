# 员工信息管理的视图文件
from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from myadmin.models import User
from django.db.models import Q #Q专门用来封装或的操作
from datetime import datetime
from django.shortcuts import redirect
from django.urls import reverse
import hashlib,random
# Create your views here.

def index(request,pindex=1):
    """浏览信息"""
    #浏览信息，浏览的是类变量
    umod=User.objects
    # l=umod.all()
    # for u in l:
    #     print(u.id,u.status,u.username)
    ulist=umod.filter(status__lt=9) #lte表示小于等于9，lt表示小于9,实现数据假删除
    #获取并判断搜索条件
    kw=request.GET.get("keyword",None)
    mywhere=[] #维持搜索条件
    if kw :
        ulist = ulist.filter(Q(username__contains=kw) | Q(nickname__contains=kw))
        mywhere.append('keyword='+kw)
    # if kw or status!= "":
    #     ulist = ulist.filter((Q(username__contains=kw) | Q(nickname__contains=kw)) & Q(status=status))
    #     mywhere.append('keyword='+kw)
    #     mywhere.append("status=" + status)
    #获取、判断并封装状态status搜索条件
    # for u in ulist:
    #     print(u.id,u.status,u.username)
    status=request.GET.get("status","")
    if status !="":
        ulist=ulist.filter(status=status)
        mywhere.append("status="+status)
    #执行分页处理
    pindex=int(pindex)
    page = Paginator(ulist,5) #以每页五条数据分页
    maxpages = page.num_pages #获取最大页数
    #判断当前页是否越界
    if pindex>maxpages:
        pindex=maxpages
    if pindex<1:
        pindex=1
    ulist2=page.page(pindex) #获取当前页数据
    plist=page.page_range #获取页面列表信息
    context={"userlist":ulist2,"pindex":pindex,"plist":plist,"maxpages":maxpages,"mywhere":mywhere}
    return render(request,"myadmin/user/index.html",context)

def add(request):
    """加载信息添加表单"""
    return render(request,"myadmin/user/add.html")

def insert(request):
    """执行信息添加"""
    #添加、修改信息，改的是对象中的实例变量
    try:
        ob=User()
        ob.username = request.POST.get("username")
        ob.nickname = request.POST.get("nickname")
        userinfo = User.objects.filter(Q(username=ob.username) | Q(nickname=ob.nickname))
        #print(userinfo)
        if userinfo.exists():
            context = {"info": "账户名称或昵称重复!"}
            return render(request, "myadmin/info.html", context)
        #判断两次密码输入是否一致
        pw1=request.POST['password']
        pw2=request.POST['repassword']
        print(bool(pw1==pw2))
        if pw1 == pw2:
            #获取密码并md5
            md5 = hashlib.md5()
            n = random.randint(100000, 999999)
            s = request.POST['password']+str(n) #从表单中获取密码并添加干扰值
            md5.update(s.encode('utf-8')) #将要产生的md5的子串放进去
            ob.password_hash = md5.hexdigest() #获取md5值
            ob.password_salt = n
            ob.status = 1
            ob.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ob.save()
            context={"info":"添加成功!"}
        else:
            context = {"info": "两次密码输入不一致!"}
    except Exception as err:
        print(err)
        context={"info":"添加失败!"}
    return render(request,"myadmin/info.html",context)

def delete(request,uid=0):
    """执行信息删除"""
    try:
        ob = User.objects.get(id=uid)
        ob.status = 9
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {"info": "删除成功!"}
    except Exception as err:
        print(err)
        context = {"info": "删除失败!"}
    return render(request, "myadmin/info.html", context)

def edit(request,uid=0):
    """加载信息编辑表单"""
    try:
        ob = User.objects.get(id=uid)
        ob.save()
        context = {"user": ob}
        return render(request, "myadmin/user/edit.html", context)
    except Exception as err:
        print(err)
        context = {"info": "未找到要修改的信息!"}
        return render(request, "myadmin/info.html", context)

def resetcode(request):
    try:
        #根据登录账号获取登录信息
        user=User.objects.get(username=request.POST['username'])
        print(user.status)
        #判断当前用户是否是管理员
        if user.status == 6:
            md5 = hashlib.md5()
            n = random.randint(100000, 999999)
            s = request.POST['password']+str(n) #从表单中获取密码并添加干扰值
            md5.update(s.encode('utf-8')) #将要产生的md5的子串放进去
            #user.password_hash = User.objects.update(password_hash=md5.hexdigest())  # 获取md5值
            user.password_hash = md5.hexdigest() #获取md5值
            user.password_salt = n
            pw1 = request.POST['password']
            pw2 = request.POST['repassword']
            print(bool(pw1 == pw2))
            if pw1 == pw2:
                user.save()
                return redirect(reverse("myadmin_login"))
            else:
                context = {"info": "两次密码输入不一致!"}
        else:
            context = {"info": "无效的登录账号"}
    except Exception as err:
        print(err)
        context={"info":"登录账号不存在"}
    return render(request,"myadmin/user/resetcode.html",context)
    # user = User.objects.get(username=request.POST['username'])
    # ob = User()
    # if user.status == 6:
    #     # 获取密码并md5
    #     md5 = hashlib.md5()
    #     n = random.randint(100000, 999999)
    #     s = request.POST.get('password') + str(n)  # 从表单中获取密码并添加干扰值
    #     md5.update(s.encode('utf-8'))  # 将要产生的md5的子串放进去
    #     user.password_hash=User.objects.update(password_hash = md5.hexdigest())# 获取md5值
    #     ob.save()
    #     return redirect(reverse("myadmin_login"))
    # else:
    #     context = {"info": "修改失败!"}
    # return render(request, "myadmin/user/resetcode.html", context)



def update(request,uid=0):
    """执行信息删除"""
    try:
        ob = User.objects.get(id=uid)
        ob.nickname = request.POST.get("nickname")
        ob.status = request.POST.get("status")
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {"info": "修改成功!"}
    except Exception as err:
        print(err)
        context = {"info": "修改失败!"}
    return render(request, "myadmin/info.html", context)

