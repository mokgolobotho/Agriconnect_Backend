from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        "id",
        "username",
        "first_name",
        "last_name",
        "email",
        "cell_number",
        "gender",
        "title",
    )
    search_fields = ("username", "email", "cell_number")
    list_filter = ("gender", "title")

@admin.register(Farm)
class FarmAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "suburb",
        "city",
        "province",
        "country",
        "approximate_size",
        "latitude",
        "longitude",
    )
    search_fields = ("name", "city", "province", "country")
    list_filter = ("province", "country")

@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "farm",
        "name",
        "planting_date",
        "harvest_date",
        "quantity",
        "created_at",
        "updated_at",
        "photoperiod",
    )
    search_fields = ("name",)
    list_filter = ("farm",)

@admin.register(UserFeedback)
class UserFeedbackAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "message",
        "rating",
        "created_at",
    )
    list_filter = ("created_at",)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "title",
        "message",
        "created_at",
        "sent_at",
    )
    list_filter = ("created_at",)

@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "crop",
        "farm",
        "random_seed",
    )
    search_fields = ("farm",)
    list_filter = ("farm",)

@admin.register(SensorData)
class SensorDataAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "sensor",
        "temperature",
        "rainfall",
        "ph",
        "light_hours",
        "light_intensity",
        "rh",
        "nitrogen",
        "phosphorus",
        "potassium",
        "yield_value",
        "category_ph",
        "soil_type",
        "season",
        "n_ratio",
        "p_ratio",
        "k_ratio",
        "plant_name",
        "photoperiod",
        "recorded_at",
    )

@admin.register(FertilityRecord)
class FertilityRecordAdmin(admin.ModelAdmin):
    list_display = (
        "sensor",
        "sensor_data",
        "fertility_level",
        "recommendations",
        "created_at",
    )
    search_fields = ("sensor",)
    list_filter = ("sensor",)

@admin.register(UserDevice)
class UserDeviceAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "name",
        "fcm_token",
        "created_at",
        "updated_at",
        "active",
    )
    search_fields = ("user",)
    list_filter = ("user",)

@admin.register(WeatherAlert)
class WeatherAlertAdmin(admin.ModelAdmin):
    list_display = (
        "farm",
        "severity",
        "weather_code",
        "alert_title",
        "recommendation",
        "timestamp",
    )
    search_fields = ("severity",)
    list_filter = ("severity",)
