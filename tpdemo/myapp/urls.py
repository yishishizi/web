from django.urls import path
from . import views
urlpatterns = [
    path("",views.index,name='index'),
    #模板语法测试路由
    path("demo1",views.demo1,name='demo1'),
    #模板继承测试路由
    path("demo2",views.demo2,name='demo2'),
    path("showdistrict/",views.showdistirct,name="showdistirct"), #加载网页
    path('district/<int:uid>', views.district, name='district'),  #Ajax加载城市信息
    #path('selectcity', views.selectcity, name='selectcity')

]