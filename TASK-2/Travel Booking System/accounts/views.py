from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .models import *
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.decorators import login_required
import requests
from datetime import datetime
import razorpay
from django.conf import settings

@login_required(login_url='/accounts/login')
def home(request):
    return render(request, 'home.html')


def login_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.filter(username = email)

        if not user.exists():
            messages.warning(request,'Account not found')
            return HttpResponseRedirect(request.path_info)
        
        profile = Profile.objects.filter(user = user[0])
        if not profile.exists() or not profile[0].is_email_verified:
            messages.warning(request, 'Account not verified')
            return HttpResponseRedirect(request.path_info)
        
        user = authenticate(username = email,password = password)
        if user:
            login(request,user)
            return redirect('/')

        messages.warning(request,'Invalid credentials')
        return HttpResponseRedirect(request.path_info)
    

    return render(request,'login.html')


def register_page(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user= User.objects.filter(username = email)

        if user.exists():
            messages.warning(request,'Email already taken')
            return HttpResponseRedirect(request.path_info)
        
        user = User.objects.create(
             first_name = first_name,
             last_name = last_name,
             email = email,
             username = email
        )
        user.set_password(password)
        user.save()
        messages.success(request,'An email has been sent to your gmail')
        return HttpResponseRedirect(request.path_info)
    
    return render(request,'register.html')


def logout_page(request):
    logout(request)
    return redirect('/accounts/login')

def activate_email(request,email_token):
    try:
        user = Profile.objects.get(email_token = email_token)
        user.is_email_verified = True
        user.save()
        return redirect('/accounts/login')
    except Exception as e:
        return HttpResponse('Invalid Email Token')

def pay(request):
    if request.method == 'POST':
        amount=5000
        order_currency= 'INR'
        client = razorpay.Client(auth=(settings.KEY, settings.SECRET))
        payment = client.order.create(dict(amount=amount, currency=order_currency, payment_capture=1))
    return render(request,'prac.html')    



