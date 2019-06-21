from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, "login/index.html")

def welcome(request):
    if 'id' in request.session:
        return render(request, "login/dashboard.html")
    else:
        return redirect("/")

def register(request):
    if request.method =="GET":
        return redirect("/")
    if request.method == "POST":
        errors = User.objects.basic_validatior(request.POST)
        
        if len(errors) >0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/")
        new_user = User.objects.create_user(request.POST)
        request.session['id'] = new_user.id
        request.session['first_name'] = new_user.first_name
        return redirect("/dashboard")
        

def validate_login(request):
    try:
        user = User.objects.get(email=request.POST['email_login']) 
        
    except:
        messages.error(request, "No user with that email registered" )
        return redirect("/") 
    if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
        request.session['id'] = user.id
        request.session['first_name'] = user.first_name
        return redirect("/dashboard")
    else:
        messages.error(request, "password incorrect" )
        return redirect("/")

def logout(request):
    try:
        del request.session['id']
        del request.session['first_name']
    except:
        pass
    return redirect("/")

def email(request):
    context = {
        "found" : False
    }

    email = request.GET['email']
    user = User.objects.filter(email=email)
    if user:
        context['found'] = True
    return render(request, 'login/partials/email.html', context)

def dashboard(request):
    user_id=request.session['id']
    user = User.objects.get(id=user_id),
    context = {
        "user": user,
        "trips_attending": Trip.objects.all().filter(attendee=user_id).order_by("-created_at"),
        "other_trips": Trip.objects.exclude(attendee=user_id).order_by("-created_at"),
    }
    return render(request, "login/dashboard.html", context)

def trips(request, trip_id):
    context = {
        "trip" : Trip.objects.get(id=trip_id)
    }

    return render(request, "login/trip.html", context)

def remove_trip(request, trip_id):
    trip = Trip.objects.get(id=trip_id)
    trip.delete()
    return redirect("/dashboard")

def new_trip(request):
        return render(request, "login/new.html")
        
def create_trip(request):
    if request.method =="GET":
        return redirect("/dashboard")
    if request.method == "POST":
        errors = User.objects.trip_validator(request.POST)
        if len(errors) >0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/trips/new")
    
    plan = request.POST['plan']
    
    d_name = request.POST['destination']
    destination = Destination.objects.create(name=d_name)

    planner = User.objects.get(id=request.session['id'])

    start = request.POST['start']
    end = request.POST['end']
    
    trip = Trip.objects.create(plan=plan, planner=planner , destination=destination, start=start, end=end)
    trip.attendee.add(planner)
    return redirect("/dashboard")

def edit_trip(request, trip_id):
    context = {
        "trip" : Trip.objects.get(id=trip_id)
    }
    return render(request, "login/edit.html", context)

def submit_edit(request, trip_id):
    if request.method =='POST':
        errors = User.objects.trip_validator(request.POST)
        if len(errors) >0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(f"/trips/{trip_id}/edit")
        trip = Trip.objects.get(id=trip_id)
        trip.plan =request.POST['plan']
        trip.start = request.POST['start']
        trip.end = request.POST['end']
        trip.destination = Destination.objects.create(name=request.POST['destination'])
        trip.save()
    return redirect("/dashboard")

def join(request, trip_id):
    trip = Trip.objects.get(id=trip_id)
    user = User.objects.get(id=request.session['id'])
    print(trip.plan)
    print(user.first_name)
    trip.attendee.add(user)

    return redirect("/dashboard")

def cancel(request, trip_id):
    trip = Trip.objects.get(id=trip_id)
    user = User.objects.get(id=request.session['id'])
    print(trip.plan)
    print(user.first_name)
    trip.attendee.remove(user)

    return redirect("/dashboard")


