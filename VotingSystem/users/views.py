from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Ext_User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def reg(req):
    if req.method == 'POST':
        firstname = req.POST.get('FirstName')
        lastname = req.POST.get('LastName')
        username = req.POST.get('username')
        email = req.POST.get('email')
        password = req.POST.get('password')
        gender = req.POST.get('gender')
        profession = req.POST.get('profession')

        u = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=firstname,
            last_name=lastname
        )

        Ext_User.objects.create(
            user_id=u,
            gender=gender,
            profession=profession
        )

        return redirect('login')

    return render(req, 'users/regist.html')



def user_login(req):
    if req.method == 'POST':
        identifier = req.POST.get('username')
        password = req.POST.get('password')

        username = None

        if identifier:
            if "@" in identifier:
                try:
                    user_obj = User.objects.get(email=identifier)
                    username = user_obj.username
                except User.DoesNotExist:
                    pass
            else:
                username = identifier

        if username:
            user = authenticate(req, username=username, password=password)
        else:
            user = None

        if user is not None:
            login(req, user)
            return redirect('home')
        else:
            messages.error(req, "Invalid username or password")

    return render(req, 'users/login.html')


def user_logout(req):
    logout(req)
    messages.success(req, "Logged out successfully!")
    return redirect('login')



def forget_password(req):
    return render(req, 'users/forget_password.html')



def otp(req):
    return render(req,'users/otp.html')

def reset_password(req):
    return render(req,'users/reset_password.html')
