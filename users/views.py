from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from users.forms import UserRegisterForm
from .models import User
from django.http import HttpResponse
from datetime import date
from django.core.files.storage import FileSystemStorage
import random
from django.http import HttpResponse
from collections import OrderedDict

def index(request): # main page rendered for any request
    return render(request, 'index.html')

def info(request): # website introduction page
    return render(request, 'info.html')

def signup(request): # sign up 
    if (request.method =="POST"): 
        email = request.POST.get('email')
        password1 = request.POST.get('passw')
        password2 = request.POST.get('passw-repeat')
        if(request.POST.get('owner')!= None): # check boxes to build up identities for users
            group = 1 # car owner
        else:
            group = 2  # admin
        if(password1 == password2): # emai define as unique, only check password
            user = User.objects.create(email=email,password=password1,group=group)
            if(group == 1): # redirect the car owner to registration
                return redirect(registration, email=email)
            else:
                return redirect(search) # admin to full searching page
    return render(request, 'signup.html')

def login(request):
    if (request.method =="POST"):
        email = request.POST.get('email') #get( input name from html page)
        passw = request.POST.get('passw')
        user = User.objects.get(email=email) # find the match object
        if (user.password == passw): # the password is valid via searching user email as a key
            if (user.group == 1):
                return redirect(profile, email=email) #pass a variable to the next profile view
            else:
                return redirect(search)         
    return render(request, 'login.html')
    

def registration(request, email): # accpet the parameter from login method
    if (request.method =="POST"): # post request in form in html invoke data saving function
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
        profile_image = request.FILES['profile_image'] # get a file from html
        fs = FileSystemStorage() # save file 
        image = fs.save(profile_image.name, profile_image)
        link = fs.url(image) # build up the unique link for each user and their image
        user = User.objects.filter(email=email).update(image = link, name=name,dob=dob,address=address,phone=phone,license=license,
        car_make=car_make,car_model=car_model,car_year=car_year,car_colour=car_colour,car_county=car_county, car_plate=car_plate)
        return redirect(profile, email=email) # submit successfully, then redirect to profile.html
    return render(request, 'registration.html', locals()) # return the local variables to html page

def profile(request, email): # the logic for recognize the car owner details
    if (request.method =="POST"):
        user = User.objects.get(email=email)
        return redirect(registration, email=user.email)
    user = User.objects.get(email=email)
    today = date.today() # to calculate the age based on the diffence between user data of birth and current data
    user.age = today.year - user.dob.year
    return render(request, 'profile.html', locals())

def search(request): # full search page
    if (request.method =="POST"):
        car_plate = request.POST['car_plate']
        user = User.objects.get(car_plate=car_plate) # only return the user object by full matched car plate
        today = date.today()
        user.age = today.year - user.dob.year
    return render(request, 'search.html', locals())

def partial(request):  # partial searching function
    if (request.method =="POST"):
        plate = request.POST['partial_plate']
        users = User.objects.filter(car_plate__contains=plate) # a filter used for Django ORM technique
    return render(request, 'partial.html', locals())  # return users which is an array

def partialDetail(request, car_plate): #the car_plate is from implemented url 
    owner = User.objects.get(car_plate=car_plate)
    today = date.today()
    owner.age = today.year - owner.dob.year
    return render(request,'partial.html', locals()) # the partial.html will show the car owner details

def availability(request, email): # take the email from url fetch the user for info in this page
    if (request.method =="POST"):
        user = User.objects.get(email=email) # get to know the user
        innum = request.POST.get('psearch', False) # save the input string as innum
        for each in User.objects.all(): # interate each users in database
            if (innum == each.car_plate): # any occupied car plate
                message = "The plate is not avaliable."
                print(message) # return the non avaliable message
                break # interrupt the loop to improve efficiency of searching
        else:
            message = "The plate is avaliable."
            print(message) # return the avaliable message
        if (message == "The plate is not avaliable."): # the logic for providing random avaliable car plate number
            infoArray = [user.name, user.phone, str(user.dob)] # array to create familiar car plate 
            suggestSet = set() # empty container for collecting avaliable numbers
            while len(suggestSet) < 10: # keep searching until there are 10 avaliable numbers
                choice=random.randrange(0, len(infoArray)) # choose any index of infoArray 
                compositeArr=[random.randrange(0,2),choice, random.randrange(1,len(infoArray[choice]))]#front/back, choice, char number#
                if (compositeArr[0]==0):
                    suggestNum = infoArray[choice][0:compositeArr[2]] + innum # infoArray[choice] is a string, add random numbers of char from the front
                else:
                    suggestNum = innum + infoArray[choice][0:compositeArr[2]]
                        
                for item in User.objects.all(): # sending the car plate numbers after checking its availability again
                    if (suggestNum == item.car_plate):
                        break # avoid saved into the presenting array(suggestSet)
                else:
                    suggestSet.add(suggestNum) 
    return render(request, 'plateavailability.html', locals())


