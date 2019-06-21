from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
from datetime import datetime, date, timezone
from django.contrib.sessions.backends.db import SessionStore


class UserManager(models.Manager):
    def basic_validatior(self, postData):
        EMAIL_RE = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        PW_RE= r'^(?=.*[!@#$%^&*?])(?=.*[a-z])(?=.*[A-Z]).{8,20}$'
        today = date.today()
        born = datetime.strptime(postData['birthday'], '%Y-%m-%d')
        errors = {}

        if len(postData['first_name']) < 2:
            errors['first_name'] = "first name too short"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "last name too short"
        if not re.match(EMAIL_RE, postData['email']):
            errors['email'] = "please enter a valid email"
        if not re.match(PW_RE, postData['password']):
            errors['password'] = "Password must have at least 1 lowercase, 1 uppercase and one special character"
        if len(postData['password']) < 8:
            errors['password'] = "password too short"
        if User.objects.filter(email =postData['email']):
            errors['email_taken'] = "email taken"
        if (today.year - born.year - ((today.month, today.day) < (born.month, born.day))) < 13:
            errors['birthday'] = "Must be 13 or older to register"
      
        return errors

    def trip_validator(self, postData):
        errors ={}
        today = datetime.today()
        print()
        start = datetime.strptime(postData['start'], '%Y-%m-%d')
        end = datetime.strptime(postData['end'], '%Y-%m-%d')
        start1 = postData['start']
        # print(type(start))
        # print(type(today))
 
        dest = postData['destination']
        start = postData['start']
        end = postData['end']
        plan = postData['plan']

        if len(dest) < 3:
            errors['destination'] = "Destinations must be atleast 3 characters long."
        if len(plan) < 3:
            errors['plan'] = "Plans must be atleast 3 characters long."
        if start > end:
            errors['start'] = "plans must start befor they begin."
        if start < today.strftime('%Y-%m-%d'):
            errors['start'] = "No time travelling"


        return errors
        
        
        
        
        
    
    def create_user(self, postData):
        fname = postData['first_name']
        lname = postData['last_name']
        email = postData['email']
        hash1 = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
        u = User.objects.create(first_name=fname, last_name=lname, email =email, password=hash1)
        return u

class User(models.Model):
    first_name = models.CharField(max_length=55)
    last_name = models.CharField(max_length=55)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Destination(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class Trip(models.Model):
    plan = models.TextField()
    attendee = models.ManyToManyField(User, related_name="trips_joined")
    planner = models.ForeignKey(User, related_name="trip_planned")
    destination = models.ForeignKey(Destination, related_name="trips_to")
    start = models.DateField()
    end = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

        


# Create your models here.

