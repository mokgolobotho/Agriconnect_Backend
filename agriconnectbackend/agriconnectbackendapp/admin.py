from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Farm

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
