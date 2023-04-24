from django.http import HttpResponse
from django.shortcuts import render

data = {
    'showjob': ['job1','job2']
}

def signup(request):
    return HttpResponse("Hi there")

def signin(request):
    return HttpResponse("Welcome Back!")

def showjob(request):
    return render(request, 'showjob/showjob.html', data)