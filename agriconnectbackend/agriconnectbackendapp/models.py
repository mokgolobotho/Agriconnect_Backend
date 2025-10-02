from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.
class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True) 
    email = models.EmailField(unique=True)                   
    cell_number = models.CharField(max_length=20, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10)
    title = models.CharField(max_length=10)
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    class Meta:
        db_table = "User"


class Farm(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name="farms"
    )
    name = models.CharField(max_length=255)
    suburb = models.CharField(max_length=255, blank=True, null=True)  
    city = models.CharField(max_length=255, blank=True, null=True) 
    province = models.CharField(max_length=255, blank=True, null=True)   
    country = models.CharField(max_length=255, blank=True, null=True)  
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    length = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    width = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    approximate_size = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = "Farm"

class Crop(models.Model):
    farm = models.ForeignKey(
        'Farm',
        on_delete=models.CASCADE,
        related_name='crops'
    )
    name = models.CharField(max_length=255)
    planting_date = models.DateField(blank=True, null=True)
    harvest_date = models.DateField(blank=True, null=True)
    quantity = models.FloatField(blank=True, null=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "Crops"

class UserFeedback(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='feedbacks'
    )
    message = models.TextField()
    rating = models.PositiveSmallIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "Feedback"
        ordering = ['-created_at']

class Notification(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    title = models.CharField(max_length=255)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "Notification"