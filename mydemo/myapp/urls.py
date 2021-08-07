from django.urls import path,re_path
from myapp import views

urlpatterns = [
    path('',views.index,name="index"),
    path('add/',views.add,name="add"),
    path('find/<int:sid>/<str:name>',views.find,name="find3"),
    re_path(r"^fun/?P<y>([0-9]{4})/?P<m>([0-9]{2})$",views.fun),
    path('update/',views.update),
<<<<<<< HEAD
=======
<<<<<<< HEAD
=======
    path("upload",views.upload,name="upload"),
    path("show",views.show,name="show"),
    path("delete",views.deleteph,name="delete"),

>>>>>>> d984aa5 (second commit)
>>>>>>> 5548d7a (second commit)

]