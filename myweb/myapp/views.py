from django.shortcuts import render
from django.http import HttpResponse
from myapp.models import student
# Create your views here.
def index(request):
    return HttpResponse("Hello world")

def add(request):
    lists=student.objects.all()
    for stu in lists:
        print(stu)
    print(student.objects.get(id=5))
    return HttpResponse("add....")
