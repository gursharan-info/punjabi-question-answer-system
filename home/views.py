from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request,  'home/index.html', {})

def projects(request):
    return render(request,  'home/projects.html', {})

def interests(request):
    return render(request,  'home/interests.html', {})

def about(request):
    return render(request,  'home/about.html', {})

def academic(request):
    return render(request,  'home/academic.html', {})

def personal(request):
    return render(request,  'home/personal.html', {})