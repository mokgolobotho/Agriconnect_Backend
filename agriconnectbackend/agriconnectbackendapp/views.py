from django.shortcuts import render
from rest_framework import generics, status
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import connection
from django.contrib.auth.hashers import check_password


# Create your views here.
class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response(
                {'error': 'Username and password are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM user WHERE username = %s", [username])
            columns = [col[0] for col in cursor.description]
            row = cursor.fetchone()
            
            if row:
                row = dict(zip(columns, row))

        if row is None:
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )


        # 🔹 Check Django-hashed password
        if (password != row['password']):
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        user = User.objects.get(pk=row['id'])
        serializer = UserSerializer(user)

        return Response(
            {'message': 'Login successful', 'user': serializer.data},
            status=status.HTTP_200_OK
        )

class AddFarm(APIView):
    def post(self, request):
        try:
            # You can either use the logged-in user or fetch by ID
            owner_id = request.data.get("owner_id")
            name = request.data.get("name")
            suburb = request.data.get("suburb")
            city = request.data.get("city")
            province = request.data.get("province")
            country = request.data.get("country")
            latitude = request.data.get("latitude")
            longitude = request.data.get("longitude")
            length = request.data.get("length")
            width = request.data.get("width")
            approximate_size = request.data.get("approximate_size")

            # Validate required fields
            if not owner_id or not name:
                return Response(
                    {"error": "owner_id and name are required."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Ensure owner exists
            try:
                owner = User.objects.get(pk=owner_id)
            except User.DoesNotExist:
                return Response(
                    {"error": "Owner not found."},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Create the farm record
            farm = Farm.objects.create(
                owner=owner,
                name=name,
                suburb=suburb,
                city=city,
                province=province,
                country=country,
                latitude=latitude,
                longitude=longitude,
                length=length,
                width=width,
                approximate_size=approximate_size,
            )

            # Return success
            return Response(
                {
                    "message": "Farm created successfully.",
                    "farm": {
                        "id": farm.id,
                        "owner": farm.owner.username,
                        "name": farm.name,
                        "suburb": farm.suburb,
                        "city": farm.city,
                        "province": farm.province,
                        "country": farm.country,
                        "latitude": farm.latitude,
                        "longitude": farm.longitude,
                        "length": str(farm.length),
                        "width": str(farm.width),
                        "approximate_size": str(farm.approximate_size),
                        "created_at": farm.created_at,
                        "updated_at": farm.updated_at,
                    }
                },
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(
                {"error": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class FarmDetail(APIView):
    def get(self, request, farm_id):
        try:
            farm = Farm.objects.get(pk=farm_id)
        except Farm.DoesNotExist:
            return Response({"error": "Farm not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = FarmSerializer(farm)
        return Response({"farm": serializer.data}, status=status.HTTP_200_OK)
    
class UserFarms(APIView):
    def get(self, request, user_id):
        farms = Farm.objects.filter(owner_id=user_id)
        serializer = FarmSerializer(farms, many=True)
        return Response({"farms": serializer.data}, status=status.HTTP_200_OK)