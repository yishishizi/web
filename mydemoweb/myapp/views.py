from django.shortcuts import render
from django.http import HttpResponse
from myapp.models import Users
from django.core.paginator import Paginator
from PIL import Image
import time,os
# Create your views here.
def index(request):
    return render(request,'myapp/index.html')
#加载文件上传表单
def upload(request):
    return render(request,'myapp/upload.html')
#执行文件上传表单页
def doupload(request):
    myflie=request.FILES.get("pic",None)#FILES只接受上传信息
    if not myflie:
        return HttpResponse("没有上传文件信息")
    # print(myflie)
    # print(request.POST.get("title"))
    #生成上传后的文件名
    filename = str(time.time()) + "." + myflie.name.split('.').pop()
    destination=open("./static/pics/"+filename,"wb+")
    for chunk in myflie.chunks():#分块读取上传文件内容并写入目标文件
        destination.write(chunk)
    destination.close()

    # 执行图片缩放
    im = Image.open("./static/pics/" + filename)
    # 缩放到75*75(缩放后的宽高比例不变):
    im.thumbnail((75, 75))
    # 把缩放后的图像用jpeg格式保存:
    im.save("./static/pics/s_" + filename, None)

    # 执行图片删除
    # os.remove("./static/pics/"+filename)

    return HttpResponse("上传的文件:"+filename)
#浏览用户信息
def indexUsers(request):
    try:
        ulist=Users.objects.all()
        context={"userslist":ulist}
        return render(request,"myapp/users/index.html",context)#加载模板
    except:
        return HttpResponse("没有找到用户信息！")

#分页浏览用户信息
def pageUsers(request,pindex=1):
    try:
        #判断搜索条件，并封装
        kw=request.GET.get("keyword",None)
        mywhere=""#定义一个用于储存搜索条件的变量
        if kw:
            list1 = Users.objects.filter(name__contains=kw)
            mywhere="?keyword=%s"%(kw)
        else:
            list1 = Users.objects.filter()
        p=Paginator(list1,5)
        #判断页码值是否有效(防止越界)
        if pindex<1:
            pindex = 1
        if pindex>p.num_pages:
            pindex=p.num_pages
        ulist = p.page(pindex)
        context={"userslist":ulist,"pindex":pindex,"pagelist":p.page_range,"mywhere":mywhere}
        return render(request,"myapp/users/index2.html",context)#加载模板
    except:
        return HttpResponse("没有找到用户信息！")

#加载添加用户信息表单
def addUsers(request):
    return render(request,"myapp/users/add.html")
#执行用户信息添加
def insertUsers(request):
    try:
        ob=Users()
        #从表单中获取要添加的信息并封装到ob对象中
        ob.name=request.POST['name']
        ob.age = request.POST['age']
        ob.phone = request.POST['phone']
        ob.save()
        context={"info":"添加成功"}
    except:
        context={"info":"添加失败"}
    return render(request, "myapp/users/info.html",context)
#执行用户信息删除
def delUsers(request,uid=0):
    try:
        ob=Users.objects.get(id=uid)#获取要删除的数据
        ob.delete()#执行删除操作
        context={"info":"删除成功"}
    except:
        context={"info":"删除失败"}
    return render(request, "myapp/users/info.html",context)
#加载用户信息修改表单
def editUsers(request,uid=0):
    try:
        ob = Users.objects.get(id=uid)  # 获取要删除的数据
        context = {"user": ob}
        return render(request, "myapp/users/edit.html", context)
    except:
        context = {"info": "没有找到要修改的数据"}
        return render(request, "myapp/users/info.html", context)
#执行用户信息修改
def updateUsers(request):
    try:
        uid=request.POST['id']#获取要修改数据的id号
        ob = Users.objects.get(id=uid)#查询要修改的数据
        # 从表单中获取要添加的信息并封装到ob对象中
        ob.name = request.POST['name']
        ob.age = request.POST['age']
        ob.phone = request.POST['phone']
        ob.save()
        context = {"info": "修改成功"}
    except:
        context = {"info": "修改失败"}
    return render(request, "myapp/users/info.html", context)
#富文本编辑器的使用
def myueditor(request):
    return render(request,"myapp/ueditor.html")