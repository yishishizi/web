from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from datetime import datetime
from myapp.models import District
# Create your views here.
def index(request):
    return render(request,"myapp/index.html")

def demo1(request):
    #模板的语法
    context={}
    context['name']='zhangsan'
    context['a']=[10,20,30]
    context['stu']={'name':"lisi","age":20}
    data=[
        {"name":"张翠山","sex":1,"age":40,"state":0},
        {"name": "殷素素", "sex": 0, "age": 38, "state": 2},
        {"name": "张无忌", "sex": 1, "age": 20, "state": 1},
        {"name": "赵敏", "sex": 0, "age": 18, "state": 2},
    ]
    context["dlist"]=data
    context['time']=datetime.now
    context['m1']=100
    context['m2']=20
    return render(request,'myapp/demo1.html',context)

def demo2(request):
    return render(request,"myapp/demo2.html")

def showdistirct(request):
    return render(request,"myapp/district.html")

#加载对应的城市信息函数，返回Json数据格式
def district(request,uid=0):
    mod=District.objects.filter(id=uid)
    mlist = []
    for mob in mod:
        mlist.append({'id': mob.id, "name": mob.name})
    print(mlist)
    dlist=District.objects.filter(upid=uid)
    mylist=[]
    for ob in dlist:
        mylist.append({'id':ob.id,"name":ob.name})
    return JsonResponse({'data':mylist})


