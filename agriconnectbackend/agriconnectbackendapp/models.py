from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from datetime import datetime


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
        db_table = "user"


class Farm(models.Model):
    id = models.AutoField(primary_key=True)
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
    code = models.IntegerField(null=True, blank= True) 
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    length = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    width = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    approximate_size = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(default=datetime.now)
    class Meta:
        db_table = "farm"

class Crop(models.Model):
    id = models.AutoField(primary_key=True)
    farm = models.ForeignKey(
        'Farm',
        on_delete=models.CASCADE,
        related_name='crops'
    )
    name = models.CharField(max_length=255)
    planting_date = models.DateField(blank=True, null=True)
    harvest_date = models.DateField(blank=True, null=True)
    quantity = models.FloatField(blank=True, null=True) 
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(default=datetime.now)
    photoperiod = models.CharField(max_length=255, default="Short Day Period") 

    class Meta:
        db_table = "crops"

class UserFeedback(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='feedbacks'
    )
    message = models.TextField()
    rating = models.PositiveSmallIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now)
    class Meta:
        db_table = "Feedback"
        ordering = ['-created_at']

class Notification(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    title = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    sent_at = models.DateTimeField(default=datetime.now)
    class Meta:
        db_table = "notification"

class Sensor(models.Model):
    id = models.AutoField(primary_key=True)
    crop = models.ForeignKey(
            'Crop',
            on_delete= models.CASCADE,
            related_name='sensor'
    )
    farm = models.ForeignKey(
        'Farm',
        on_delete=models.CASCADE,
        related_name='sensor'
    )
    random_seed = models.IntegerField()
    class Meta:
        db_table  = "sensor"

class SensorData(models.Model):
    id = models.AutoField(primary_key=True)
    sensor = models.ForeignKey(
        Sensor,
        on_delete=models.CASCADE,
        related_name='data'
    )
    temperature = models.FloatField()
    rainfall = models.FloatField()   
    ph = models.FloatField()               
    light_hours = models.FloatField()      
    light_intensity = models.FloatField()  
    rh = models.FloatField()
    nitrogen = models.FloatField()
    phosphorus = models.FloatField()
    potassium = models.FloatField()
    yield_value = models.FloatField()
    category_ph = models.CharField(max_length=50)
    soil_type = models.CharField(max_length=50)
    season = models.CharField(max_length=50)
    n_ratio = models.FloatField()
    p_ratio = models.FloatField()
    k_ratio = models.FloatField()
    plant_name = models.CharField(max_length=100)
    photoperiod = models.CharField(max_length=100)
    recorded_at = models.DateTimeField(default=datetime.now)

    class Meta:
        db_table = "sensor_data"


class FertilityRecord(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name="fertility_records")
    sensor_data = models.OneToOneField(SensorData, on_delete=models.CASCADE, related_name="fertility_record")
    fertility_level = models.CharField(max_length=50)
    recommendations = models.JSONField(default=list)
    created_at = models.DateTimeField(default=datetime.now)

    class Meta:
        db_table = "fertility_record"

class UserDevice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="devices")
    name = models.CharField(max_length=100, blank=True)
    fcm_token = models.CharField(max_length=512)
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(default=datetime.now)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = "user_device"

class WeatherAlert(models.Model):
    SEVERITY_CHOICES = (
        ("HIGH", "High"),
        ("EXTREME", "Extreme"),
    )

    farm = models.ForeignKey(Farm, on_delete=models.CASCADE)
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES)
    weather_code = models.IntegerField()
    alert_title = models.CharField(max_length=100)
    recommendation = models.TextField()
    timestamp = models.DateTimeField(default=datetime.now)

    class Meta:
        db_table = "weather_alert"
 
