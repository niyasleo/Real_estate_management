from django.db import models


# Create your models here.
class Property_type(models.Model):
    property_types=models.CharField(max_length=20,null=True)
class Listed_properties(models.Model):
    property_id=models.IntegerField()
    property_title=models.CharField(max_length=20,null=True)
    posted_by=models.CharField(max_length=20,null=True)


class ContactMessage(models.Model):
    ROLE_CHOICES = [
        ('buyer', 'Buyer / Renter'),
        ('owner', 'Property Owner'),
        ('agent', 'Real Estate Agent'),
    ]

    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    subject = models.CharField(max_length=200, blank=True, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name



