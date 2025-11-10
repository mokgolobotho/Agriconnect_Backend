from django.shortcuts import render
from rest_framework import generics, status
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import connection
from django.contrib.auth.hashers import check_password
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .ml_model.model import predict_fertility, predict_name
from .ml_model.recommendations import generate_recommendations
import random
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth import logout


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
        try:
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
        except Exception as e:
            return Response(
                {"error": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class AddFarm(APIView):
    def post(self, request):
        try:
            owner_id = request.data.get("owner_id")
            name = request.data.get("name")
            suburb = request.data.get("suburb")
            city = request.data.get("city")
            province = request.data.get("province")
            country = request.data.get("country")
            code = request.data.get("code")
            latitude = request.data.get("latitude")
            longitude = request.data.get("longitude")
            length = request.data.get("length")
            width = request.data.get("width")
            approximate_size = request.data.get("approximate_size")
            
            try:
                owner = User.objects.get(pk=owner_id)
            except User.DoesNotExist:
                return Response(
                    {"error": "Owner not found."},
                    status=status.HTTP_404_NOT_FOUND
                )

            farm = Farm.objects.create(
                owner=owner,
                name=name,
                suburb=suburb,
                city=city,
                province=province,
                country=country,
                code=code,
                latitude=latitude,
                longitude=longitude,
                length=length,
                width=width,
                approximate_size=approximate_size,
            )

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
            serializer = FarmSerializer(farm)
            return Response({"farm": serializer.data}, status=status.HTTP_200_OK)
        except Farm.DoesNotExist:
            return Response({"error": "Farm not found"}, status=status.HTTP_404_NOT_FOUND)
    
class UserFarms(APIView):
    def get(self, request, user_id):
        try:
            farms = Farm.objects.filter(owner_id=user_id)
            serializer = FarmSerializer(farms, many=True)
            return Response({"farms": serializer.data}, status=status.HTTP_200_OK)
        except Farm.DoesNotExist:
            return Response(
                {"error": "They are no farms"}, status=status.HTTP_404_NOT_FOUND
            )
    
class AddCrop(APIView):
    def post(self, request):
        try:
            farm_id = request.data.get("farm_id")
            name = request.data.get("name")
            planting_date = request.data.get("planting_date")
            harvest_date = request.data.get("harvest_date")
            quantity = request.data.get("quantity")
            created_at = request.data.get("created_at")
            updated_at = request.data.get("updated_at")

            try:
                farm = Farm.objects.get(pk=farm_id)
            except(Farm.DoesNotExist):
                return Response(
                    {"error: farm does not exist"},
                    status=status.HTTP_404_NOT_FOUND
                )
            photoperiod = predict_name(name)
            crop = Crop.objects.create(
                farm = farm,
                name = name,
                planting_date = planting_date,
                harvest_date = harvest_date,
                quantity = quantity,
                created_at = created_at,
                updated_at = updated_at,
                photoperiod = photoperiod,
            )
            random_seed = random.choice(range(10, 901, 10))

            sensor = Sensor.objects.create(
                farm=farm,
                crop=crop,
                random_seed=random_seed
            )

            return Response({
                "message": "Crop and sensor added successfully",
                "crop": {
                    "id": crop.id,
                    "name": crop.name,
                    "photoperiod": crop.photoperiod
                },
                "sensor": {
                    "id": sensor.id,
                    "random_seed": sensor.random_seed
                }
            },
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {"error": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
class FarmCrops(APIView):
    def get(self, request, farm_id):
        try:
            farmCrops = Crop.objects.filter(farm_id= farm_id)
            if farmCrops.exists():
                serializer = CropSerializer(farmCrops, many=True)
                return Response({"crops": serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"error": "No crops found for this farm"}, status=status.HTTP_404_NOT_FOUND
                )
        except Crop.DoesNotExist:
            return Response(
                {"error": "crops do not exist"}, status=status.HTTP_404_NOT_FOUND
            )
class GetCrop(APIView):
    def get(self,request, crop_id):
        try:
            crop = Crop.objects.get(pk = crop_id)
            return Response(
                {"crop": crop}, status=status.HTTP_200_OK
            )
        except Crop.DoesNotExist:
            return Response(
                {"error": "crops do not exist"}, status=status.HTTP_404_NOT_FOUND
            )


class AddFeedback(APIView):
    def post(self,request):
        try:
            user_id = request.data.get("owner_id")
            message = request.data.get("message")
            rating = request.data.get("rating")
            created_at = request.data.get("created_at")
            try:
                user = User.objects.get(pk=user_id)
            except User.DoesNotExist:
                return Response(
                    {"error": "Owner not found."},
                    status=status.HTTP_404_NOT_FOUND
                )
            feedback = UserFeedback.objects.create(
                user = user,
                message = message,
                rating = rating,
                created_at = created_at,                         
                )
            
            return Response(
                {"message": "logged successfully "}, status= status.HTTP_201_CREATED 
            )
        except Exception as e:
            return Response(
                {"error": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
class CreateNotification(APIView):
    def post(self, request):
        try:
            user_id = request.data.get("user_id")
            title = request.data.get("title")
            message = request.data.get("message")
            created_at = request.data.get("created_at")

            try:
                user = User.objects.get(pk= user_id)
            except User.DoesNotExist:
                return Response ({"error": "user not found"}, status= status.HTTP_404_NOT_FOUND)

            Notification.objects.create(
                user = user,
                title = title,
                message = message,
                created_at = created_at,                
            )
            return Response({"message": "created successfully"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": "an error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class PostNotification(APIView):
    def get(self, notification_id):
        try:
            notification = Notification.objects.get(pk = notification_id)
            return Response(
                {"Notification": notification}, status=status.HTTP_200_OK
            )
        except Notification.DoesNotExist:
            return Response(
                {"error": "Notification does not exist"}, status=status.HTTP_404_NOT_FOUND
            )

class SaveFcmToken(APIView):
    def post(self, request):
        try:
            user_id = request.data.get("user_id")
            token = request.data.get("fcm_token")

            if not user_id or not token:
                return Response(
                    {"error": "user_id and fcm_token are required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            user = User.objects.get(id=user_id)

            # Always ensure one active token per user
            UserDevice.objects.filter(user=user).delete()

            # Save the new token
            UserDevice.objects.create(
                user=user,
                fcm_token=token,
                active=True
            )

            return Response(
                {"success": True, "message": "FCM token saved successfully"},
                status=status.HTTP_200_OK
            )

        except User.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class FarmFertilityAlerts(APIView):
    def get(self, request, farm_id):
        try:
            three_days_ago = timezone.now() - timedelta(days=3)

            # Filter fertility records for this farm with low fertility in the last 3 days
            records = FertilityRecord.objects.filter(
                sensor__farm__id=farm_id,
                fertility_level__iexact='Low',
                created_at__gte=three_days_ago
            ).order_by('-created_at')

            serializer = FertilityRecordSerializer(records, many=True)

            return Response({
                "success": True,
                "farm_id": farm_id,
                "count": len(serializer.data),
                "alerts": serializer.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "success": False,
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LogoutView(APIView):
    """
    Deactivate all devices for a given user_id sent in the request body.
    """

    def post(self, request):
        try:
            user_id = request.data.get("user_id")
            if not user_id:
                return Response({
                    "success": False,
                    "message": "user_id is required."
                }, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.filter(id=user_id).first()
            if not user:
                return Response({
                    "success": False,
                    "message": "User not found."
                }, status=status.HTTP_404_NOT_FOUND)

            # Deactivate all devices
            UserDevice.objects.filter(user=user, active=True).update(active=False)

            return Response({
                "success": True,
                "message": "Devices deactivated successfully."
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "success": False,
                "message": f"Logout failed: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)