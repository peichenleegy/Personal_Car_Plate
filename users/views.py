from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from users.forms import UserRegisterForm
from .models import User
from django.http import HttpResponse
from datetime import date


def index(request):
    return render(request, 'index.html')

def info(request):
    return render(request, 'info.html')

def signup(request): # sign up after sign in?
    if (request.method =="POST"): 
        email = request.POST.get('email')
        password1 = request.POST.get('passw')
        password2 = request.POST.get('passw-repeat')
        if(request.POST.get('owner')!= None):
            group = 1
        else:
            group = 2
        if(password1 == password2):
            user = User.objects.create(email=email,password=password1,group=group)
            if(group == 1):
                return redirect(registration, email=email)
            else:
                return redirect(search)
    return render(request, 'signup.html')

def login(request):
    if (request.method =="POST"):
        email = request.POST.get('email')
        passw = request.POST.get('passw')
        user = User.objects.get(email=email)
        if (user.password == passw):
            if (user.group == 1):
                return redirect(profile, email=email)
            else:
                return redirect(search)         
    return render(request, 'login.html')
    

def registration(request, email):
    if (request.method =="POST"): 
        name = request.POST.get('name')
        dob = request.POST.get('dob')
        address = request.POST.get('address')
        phone = request.POST.get('phoneNo')
        license = request.POST.get('licenceNo')
        car_make = request.POST.get('carMake')
        car_model = request.POST.get('carModel')
        car_year = request.POST.get('carYear')
        car_colour = request.POST.get('colour')
        car_county = request.POST.get('county')
        car_plate = request.POST.get('carPlate')
        user = User.objects.filter(email=email).update(name=name,dob=dob,address=address,phone=phone,license=license,
        car_make=car_make,car_model=car_model,car_year=car_year,car_colour=car_colour,car_county=car_county, car_plate=car_plate)
    return render(request, 'registration.html')

def profile(request, email):
    if (request.method =="POST"):
        user = User.objects.get(email=email)
        return redirect(registration, email=user.email)
    user = User.objects.get(email=email)
    today = date.today()
    user.age = today.year - user.dob.year
    return render(request, 'profile.html', locals())

def search(request):
    if (request.method =="POST"):
        car_plate = request.POST['car_plate']
        user = User.objects.get(car_plate=car_plate)
        today = date.today()
        user.age = today.year - user.dob.year
    return render(request, 'search.html', locals())

def partial(request):  
    if (request.method =="POST"):
        plate = request.POST['partial_plate']
        users = User.objects.filter(car_plate__contains=plate)
    return render(request, 'partial.html', locals())  

def partialDetail(request, car_plate):
    owner = User.objects.get(car_plate=car_plate)
    today = date.today()
    owner.age = today.year - owner.dob.year
    return render(request,'partial.html', locals())


