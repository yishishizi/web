from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseNotFound,Http404,JsonResponse
from django.urls import reverse
from django.views import View
# Create your views here.
def index(request):
    return render(request,'myapp/index.html')

def resp01(request):
    return HttpResponse("<h3>一个简单的图片</h3>")

def resp02(request):
    #return HttpResponseNotFound('<h1>Page not found</h1>')#直接返回一个404，没有去加载404的模板页面
    #return HttpResponse(status=403)#直接返回一个status状态码
    return Http404("Poll does not exist")#返回一个404的错误页面
def resp03(request):
    #return redirect(reverse('resp01'))# redirect重定向  reverse反向解析url地址
    return HttpResponse('<script>alert("添加成功");location.href="/resp01";</script>')# 执行一段js代码，用js进行重定向

class Myview(View):
    def get(self,request,*args,**kwargs):
        return HttpResponse('Hello world!')

#json数据的响应
def  resp05(request):
    data=[
        {'id':10,'name':'张三','age':20},
        {'id': 11, 'name': '张四', 'age': 21},
        {'id': 12, 'name': '张五', 'age': 22},
    ]
    return JsonResponse({"data":data})

#cookie的使用
def  resp06(request):
    # #获取当前响应对象
    # #读取cookie,在第一次访问的时候，cookie是没有值的
    # response=HttpResponse('cookie的设置')
    # print(request.COOKIES.get('a',None))
    # #使用当前响应对象进行cookie的设置
    # response.set_cookie('a','abd')
    #
    # #返回响应对象
    # return response
#cookie页面计数器
    m=request.COOKIES.get('num',None)
    if m:
        m=int(m)+1
    else:
        m=1
    response=HttpResponse('cookie的设置:'+str(m))
    response.set_cookie('num',m)
    return response

def resp07(request):
    print("请求路径",request.path)
    print("请求方法",request.method)
    print("请求编码",request.encoding)
    #print(request.GET)
    print(request.GET.get('id'))
    print(request.GET.get('name'))
    print(request.GET.get('age',0))
    print(request.GET.getlist('name'))
    return HttpResponse("请求对象")

#验证码的输出
def verifycode(request):
    # 引入绘图模块
    from PIL import Image, ImageDraw, ImageFont
    # 引入随机函数模块
    import random
    # 定义变量，用于画面的背景色、宽、高
    bgcolor = (random.randrange(20, 100), random.randrange(
        20, 100), 255)
    width = 100
    height = 25
    # 创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    # 创建画笔对象
    draw = ImageDraw.Draw(im)
    # 调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    # 定义验证码的备选值
    str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    # 随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    # 构造字体对象
    font = ImageFont.truetype('static/arial.ttf', 23)
    #font = ImageFont.load_default().font
    # 构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    # 绘制4个字
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)
    # 释放画笔
    del draw
    # 存入session，用于做进一步验证
    #request.session['verifycode'] = rand_str
    # 内存文件操作
    """
    python2的为
    # 内存文件操作
    import cStringIO
    buf = cStringIO.StringIO()
    """
    # 内存文件操作-->此方法为python3的
    import io
    buf = io.BytesIO()
    # 将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    # 将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')

