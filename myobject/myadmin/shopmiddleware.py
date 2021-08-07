from django.shortcuts import redirect
from django.urls import reverse
import re
class ShopMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        print("ShopMiddleware")
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        path=request.path
        print("url:",path)

        #判断管理后台是否登录
        #定义后台允许直接访问的url列表
        urllist=['/myadmin/login','/myadmin/dologin','/myadmin/logout','/myadmin/verify']
        #判断当前请求url地址是否以/myadmin开头,并且不再urllist中，才做登录pd
        if re.match(r'^/myadmin',path) and (path not in urllist):
            #判断是否登录(在session中没有adminuser)
            if 'adminuser' not in request.session:
            #重定向到登录页
                return redirect(reverse("myadmin_login"))

        # 前台登录界面无web前缀
        #判断大堂点餐请求，判断是否登录（session中是否有webuser）
        if re.match(r'^/web',path):
            #判断是否登录(在session中没有adminuser)
            if 'webuser' not in request.session:
            #重定向到登录页
                return redirect(reverse("web_login"))

        # 判断移动端是否登录
        # 定义移动允许直接访问的url列表
        urllist = ['/mobile/register', '/mobile/doregister', '/mobile/doaddmember','/mobile/member/logout']
        # 判断当前请求url地址是否以/mobile开头,并且不再urllist中，才做登录pd
        if re.match(r'^/mobile', path) and (path not in urllist):
            # 判断是否登录(在session中没有mobileuser)
            if 'mobileuser' not in request.session:
                # 重定向到登录页
                return redirect(reverse("mobile_register"))



        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response