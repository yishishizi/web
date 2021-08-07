from django.shortcuts import render,redirect
from django.http import HttpResponse,Http404
from django.urls import reverse
<<<<<<< HEAD
=======
<<<<<<< HEAD
=======
from myapp import models
>>>>>>> d984aa5 (second commit)
>>>>>>> 5548d7a (second commit)
# Create your views here.
def index(request):
    print(reverse("add"))
    print(reverse("index"))
    print(reverse("find3",args=(100,"lisi")))
    #return redirect(reverse("find3",args=(100,"lisi")))
    return HttpResponse("Hello world!")
def add(request):
    return HttpResponse("add...")
def find(request,sid=0,name=''):
    return HttpResponse("find...%d:%s"%(sid,name))
def update(request):
    #return HttpResponse("update....")
    raise Http404("修改界面不存在")
def fun(request,y,m):
    return HttpResponse("参数信息：%s年%s月"%(y,m))
<<<<<<< HEAD
=======
<<<<<<< HEAD
=======

def upload(request):
    error = ''
    if request.method == 'POST':
        img = request.FILES.get('img')
        pic_name = img.name
        if pic_name.split('.')[-1] == 'mp4':
            error = '暂不支持上传此格式图片！！！'
        else:
            models.Images.objects.create(img_name=pic_name, img=img)#把图片上传到数据库中
            # new_img = models.mypicture(
            #     photo=request.FILES.get('photo'),  # 拿到图片
            #     user=request.FILES.get('photo').name  # 拿到图片的名字
            # )
            # new_img.save()  # 保存图片
            return redirect('show')
    return render(request, 'upload.html', locals())

def show(request):
    all_images = models.Images.objects.all()
    # for i in all_images:
    #     print(i.img)
    return render(request, 'show.html', locals())


def deleteph(request):
    pk = request.GET.get('pk')
    models.Images.objects.filter(id=pk).delete()
    return redirect('show')
>>>>>>> d984aa5 (second commit)
>>>>>>> 5548d7a (second commit)
