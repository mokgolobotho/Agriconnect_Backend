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
        fields = ['name', 'suburb', 'city', 'province', 'country', 'latitude', 'longitude', 'length', 'width', 'approximate_size', 'created_at', 'updated_at']
        read_only_fields = ['id']
