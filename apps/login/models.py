from __future__ import unicode_literals
from django.contrib import messages
from django.db import models
import bcrypt
import re
emailRegex = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
passwordRegex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$')


class UserManager(models.Manager):
    def registration(self, request):
        error = False
        if request.POST["first_name"] == "":
            messages.warning(request, "First Name is Required!")

        elif len(request.POST["first_name"]) < 2:
            messages.warning(request, "First name must be greater than 2 characters")
            error = True
        elif any(char.isdigit() for char in request.POST["first_name"]) == True:
            messages.warning(request, "First Name must be letters!")
            error = True

        if request.POST["last_name"] == "":
            messages.warning(request, "Last Name is Required!")
            error = True
        elif len(request.POST["last_name"]) < 2:
            messages.warning(request, "Last name must be greater than 2 characters")
            error = True
        elif any(char.isdigit() for char in request.POST["last_name"]) == True:
            messages.warning(request, "Last Name must be letters!")
            error = True

        if not emailRegex.match(request.POST["email"]):
            messages.warning(request, "Email is not valid!")
            error = True
        elif request.POST["email"] == "":
            messages.warning(request, "Email is required!")
            error = True
        elif User.objects.filter(email=request.POST['email']):
            messages.warning(request, "This email already exists in our database.")
            error = True

        if request.POST["password"]== "":
            messages.warning(request, "Password is Required!")
            error = True
        elif len(request.POST["password"]) < 8:
            messages.warning(request, "Password must be greater than 8 characters long")
            error = True
        elif not passwordRegex.match(request.POST["password"]):
            messages.warning(request, "Password must must contain at least one lowercase letter, one uppercase letter, and one digit!")
            error = True

        if request.POST["confirmPassword"] == "":
            messages.warning(request, "Please confirm password!")
            error = True
        elif not request.POST['password'] == request.POST['confirmPassword']:
            messages.warning(request, "Password do not match, try again!")
            error = True

        if error == False:
            request.session["first_name"] = request.POST["first_name"]
            messages.success(request, "Success! Welcome," + request.session['first_name'] + "!")
            hashed = bcrypt.hashpw(request.POST["password"].encode('utf-8'), bcrypt.gensalt())
            User.objects.create(first_name=request.POST["first_name"], last_name=request.POST["last_name"], email=request.POST["email"], password=hashed)
            print hashed
        return error

    def login(self, request):
        error = False
        if request.POST["email"] == "":
            messages.warning(request, "Email is required!")
            error = True
        elif not emailRegex.match(request.POST["email"]):
            messages.warning(request, "Email is not valid!")
            error = True

        if request.POST["password"]== "":
            messages.warning(request, "Password is Required!")
            error = True
        elif len(request.POST["password"]) < 8:
            messages.warning(request, "Password must be greater than 8 characters long")
            error = True

        if User.objects.filter(email=request.POST['email']):
            hashed = User.objects.get(email = request.POST['email']).password.encode('utf-8')
            if  bcrypt.hashpw(request.POST["password"].encode('utf-8'), hashed) == hashed:
                messages.success(request, "Success! Welcome," + request.session['first_name'] + "!")
                error = False
                print hashed
        else:
            messages.warning(request, "Unsuccessful Login, Try Again!!!")
            error = True
        return error


class User(models.Model):
        first_name = models.CharField(max_length=100)
        last_name = models.CharField(max_length=100)
        email = models.CharField(max_length=50)
        password = models.CharField(max_length=255)
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)
        objects = UserManager()
