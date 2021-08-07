from django.urls import path
from . import views

urlpatterns = [
    path('', views.index,name="index"),
    path('upload', views.upload,name="upload"),#加载文件上传表单页
    path('doupload', views.doupload,name="doupload"),#执行文件上传表单页
    path("users", views.indexUsers, name='indexusers'),
    path("pageusers/<int:pindex>", views.pageUsers, name='pageusers'),#分页浏览用户信息
    path("users/add", views.addUsers, name='addusers'),
    path("users/insert", views.insertUsers, name='insertusers'),
    path("users/del/<int:uid>", views.delUsers, name='delusers'),
    path("users/edit/<int:uid>", views.editUsers, name='editusers'),
    path("users/update", views.updateUsers, name='updateusers'),
    path("myueditor",views.myueditor,name="myueditor"),
]