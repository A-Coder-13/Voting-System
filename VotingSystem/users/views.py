from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import *
from questonaries.models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
import random
from django.utils import timezone
from datetime import timedelta


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
    if req.method == 'POST':
        email = req.POST.get('email')
        try:
            user = User.objects.get(email=email)
            otp_code = str(random.randint(100000,900000))

            PasswordOTP.objects.create(user_id=user, otp=otp_code)

            send_mail(
                "Password Reset OTP",
                f"your OTP for password reset is: {otp_code}",
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )

            req.session['reset_user'] = user.id
            return redirect('otp')
        
        except User.DoesNotExist:
            messages.error(req, "No user found with this email")
        
    return render(req, 'users/forget_password.html')



def otp(req):
    if req.method == 'POST':
        otp_code = req.POST.get('otp')
        user_id=req.session.get('reset_user')
        
        otp_obj = PasswordOTP.objects.filter(user_id=user_id,otp=otp_code).last()
        if otp_obj and otp_obj.otp==otp_code:
            return redirect('reset_password')
        else:
            messages.error(req, "Invalid OTP")

    return render(req,'users/otp.html')





def reset_password(req):
    if req.method=='POST':
        password=req.POST.get('password')
        Confirm_password=req.POST.get('confirm_password')
        if password==Confirm_password:
            user_id=req.session.get('reset_user')
            user=User.objects.get(id=user_id)
            user.set_password(password)
            user.save()
            messages.success(req, "Password reset successfully!")
            return redirect('login')
        else:
            messages.error(req, "Passwords do not match")
    return render(req,'users/reset_password.html')



def edit_profile(req):
    user= req.user

    profile, created = UserProfile.objects.get_or_create(user_id = user)

    if req.method=='POST':

        profile.profile_picture = req.FILES.get('profile_pic')
        profile.bio=req.POST.get('bio')
        profile.location = req.POST.get('location')
        profile.birth_date = req.POST.get('DOB')
        profile.save()


        user.username = req.POST.get('username')
        user.save()

        # profile.file.name=f"${username_object.username}.jpg"   for changing files name

    print(profile)
    context = {
        'profile': profile,
    }
    
    return render(req,"users/edit_profile.html",context=context)


def profile_view(req):
    try:
        profile = UserProfile.objects.get(user_id=req.user)
    except UserProfile.DoesNotExist:
        profile = None

    now = timezone.now()

    # Active polls (expiry future me)
    active_pole = Question.objects.filter(u_id=req.user, expiry__gt=now)
    t_pole = active_pole.count()

    # Total votes count
    vote_cast = 0
    for q in active_pole:
        vote_cast += Vote_Click.objects.filter(opt_id__q_id=q.id).count()

    context = {
        'profile': profile,
        'pole': t_pole,
        'votes': vote_cast
    }

    return render(req, "users/profile.html", context)