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


class PredictFertility(APIView):
    def get(self, request, crop_id):
        try:
            crop = Crop.objects.get(pk=crop_id)

            """
            # Example: get data from sensors or dummy values
            sensor_data = {
                "Name": crop.name,
                "Photoperiod": "Day Neutral",
                "Temperature": 22.5,
                "Rainfall": 700,
                "pH": 6.3,
                "Light_Hours": 12,
                "Light_Intensity": 500,
                "Rh": 90,
                "Nitrogen": 150,
                "Phosphorus": 100,
                "Potassium": 200,
                "Yield": 20,
                "Category_pH": "low_acidic",
                "Soil_Type": "Loam",
                "Season": "Summer",
                "N_Ratio": 10,
                "P_Ratio": 10,
                "K_Ratio": 10
            }
            
            sensor_data = {
                "Name": crop.name,
                "Photoperiod": "Short Day Period",
                "Temperature": 15.0,
                "Rainfall": 200,
                "pH": 5.2,
                "Light_Hours": 8,
                "Light_Intensity": 300,
                "Rh": 60,
                "Nitrogen": 50,
                "Phosphorus": 30,
                "Potassium": 40,
                "Yield": 5,
                "Category_pH": "high_acidic",
                "Soil_Type": "Sandy",
                "Season": "Winter",
                "N_Ratio": 3,
                "P_Ratio": 2,
                "K_Ratio": 4
            }
            """
            sensor_data = {
                "Name": crop.name,
                "Photoperiod": "Long Day Period",
                "Temperature": 25.0,
                "Rainfall": 800,
                "pH": 6.5,
                "Light_Hours": 14,
                "Light_Intensity": 600,
                "Rh": 85,
                "Nitrogen": 200,
                "Phosphorus": 150,
                "Potassium": 180,
                "Yield": 30,
                "Category_pH": "low_acidic",
                "Soil_Type": "Loam",
                "Season": "Summer",
                "N_Ratio": 12,
                "P_Ratio": 10,
                "K_Ratio": 12
            }


            fertility = predict_fertility(sensor_data)
            recommendations = generate_recommendations(sensor_data) if fertility != "High" else []

            return Response({
                "crop": crop.name,
                "predicted_fertility": fertility,
                "recommendations": recommendations
            }, status=status.HTTP_200_OK)
            #return Response({"crop": crop.name, "predicted_fertility": fertility}, status=status.HTTP_200_OK)

        except Crop.DoesNotExist:
            return Response({"error": "Crop not found"}, status=status.HTTP_404_NOT_FOUND)

class AddSensor(APIView):
    def post(self, request):
        try:
            crop_id = request.data.get("crop_id")
            farm_id = request.data.get("farm_id")
            random_seed = request.data.get("random_seed")
            try:
                farm = Farm.objects.get(pk=farm_id)
            except(Farm.DoesNotExist):
                return Response(
                    {"error: farm does not exist"},
                    status=status.HTTP_404_NOT_FOUND
                )
            try:
                crop = Crop.objects.get(pk=crop_id)
            except(Crop.DoesNotExist):
                return Response(
                    {"error: crop does not exist"},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            sensor =Sensor.objects.create(
                farm = farm,
                crop = crop,
                random_seed = random_seed,
            ),

            return Response({
                    "message": "sensor added",
                    "sensor" : {sensor.id}
                },
                    status=status.HTTP_201_CREATED
                )
        except Exception as e:
            return Response(
                {"error": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )