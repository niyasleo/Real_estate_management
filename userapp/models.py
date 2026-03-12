from datetime import  timedelta
from django.utils import timezone
from django.db import models

class Users(models.Model):
    Role=[('User','User'),('Agent','Agent'),('Owner','Owner')]
    role=models.CharField(choices=Role)
    name=models.CharField(max_length=30)
    mobile=models.CharField(max_length=10,unique=True)
    password=models.CharField(max_length=100)
    username=None
    USERNAME_FIELD = 'mobile'
    REQUIRED_FIELDS = []
class User_otp(models.Model):
    mobile=models.CharField(max_length=10)
    otp=models.CharField(max_length=6)
    timestamp=models.DateTimeField(auto_now_add=True)
    def is_expired(self):
        return timezone.now() > self.timestamp + timedelta(minutes=5)



class Property(models.Model):

        STATUS_CHOICES = [
        ('For SALE', 'FOR SALE'),
        ('FOR RENT', 'FOR RENT'),
        ]
        property_title = models.CharField(max_length=255,blank=True, null=True)
        location = models.CharField(max_length=255,blank=True, null=True)
        price = models.IntegerField(null=True)
        area = models.CharField(max_length=50,blank=True, null=True) # sq.m
        property_id = models.CharField(max_length=20, unique=True)
        status = models.CharField(max_length=10, choices=STATUS_CHOICES,null=True)
        bedrooms = models.CharField(max_length=50,blank=True, null=True)
        bathrooms = models.CharField(max_length=50,blank=True, null=True)
        property_type = models.CharField(max_length=50,blank=True, null=True)
        description = models.CharField(max_length=500,blank=True, null=True)
        # description=models.CharField(null=True)
        # Images
        image1 = models.ImageField(upload_to='properties_images/', blank=True, null=True)
        image2 = models.ImageField(upload_to='properties_images/', blank=True, null=True)
        image3 = models.ImageField(upload_to='properties_images/', blank=True, null=True)
        features = models.JSONField(default=list, blank=True)
        posted_by=models.CharField(max_length=20,null=True)
        posted_at = models.DateTimeField(auto_now_add=True)
        def __str__(self):
          return self.property_title

class Enquiry(models.Model):
    property_id = models.CharField(max_length=100,null=True)
    property_title = models.CharField(max_length=100,null=True)
    name = models.CharField(max_length=100,null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

