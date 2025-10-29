from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name',  'username', 'email', 'cell_number', 'password']
        read_only_fields = ['id']

class FarmSerializer(serializers.ModelSerializer):
    class Meta:
        model= Farm
        fields = ['id', 'name', 'suburb', 'city', 'province', 'country', 'latitude', 'longitude', 'length', 'width', 'approximate_size', 'created_at', 'updated_at']
        read_only_fields = ['id']

class CropSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crop
        fields = ['id', 'name', 'planting_date', 'harvest_date', 'quantity', 'photoperiod' ] 
        read_only_fields = ['id']