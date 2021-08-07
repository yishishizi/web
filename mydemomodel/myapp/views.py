from django.shortcuts import render
from django.http import HttpResponse
from myapp.models import Users
# Create your views here.
def index(request):
    #执行Model的操作

    # #添加操作
    # ob=Users()#实例化一个新对象
    # ob.name="王五"
    # ob.age=23
    # ob.phone="529894579"
    # ob.save()#新对象是添加数据，已存在的对象进行修改操作

    # #删除操作
    # mod=Users.objects#获取users的model对象
    # user=mod.get(id=6)#获取id为6的数据信息
    # print(user.name)
    # user.delete()#执行删除操作

    #修改操作
    # ob=Users.objects.get(id=7)
    # #print(ob.name)
    # ob.name="刘七"
    # ob.age=56
    # ob.save()

    #查询操作
    mod=Users.objects#获取Users模型的Model操作对象
    #ulist=mod.all()#获取所有数据
    #ulist=mod.filter(name="张三")#获取name值为张三的信息
    #ulist = mod.filter(age__gt=20)#获取age大于20的信息
    #ulist = mod.filter(age__gte=20)#获取age大于等于20的信息
    #ulist = mod.filter(age__lte=20)  # 获取age小于等于20的信息
    #ulist=mod.order_by("-age")#按age降序进行排序，升序mod.order_by("age")
    ulist=mod.order_by("age")[:3]#按age升序取前三条数据
    for u in ulist:
        print(u.id,u.name,u.age,u.phone,u.addtime)

    return HttpResponse("首页 <br/> <a href='/users'>用户信息管理</a>")

#浏览用户信息
def indexUsers(request):
    try:
        ulist=Users.objects.all()
        context={"userslist":ulist}
        return render(request,"myapp/users/index.html",context)#加载模板
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
