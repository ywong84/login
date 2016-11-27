from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User

# Create your views here.
def index(request):

    return render(request, 'login/index.html')

def create(request):
    if not User.objects.registration(request):
        return redirect ('/success')
    else:
        return redirect ('/')

def login(request):
    if not User.objects.login(request):
        return redirect ('/success')
    else:
        return redirect ('/')
def success(request):
    users= User.objects.all()
    context = {
        'users': users
    }
    return render(request, 'login/success.html', context)
