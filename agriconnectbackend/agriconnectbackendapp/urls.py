from django.urls import path
from .views import *

urlpatterns = [
    path('register/', UserListCreateView.as_view(), name='register'),
    path('users/<str:username>/', UserDetailView.as_view(), name='user-detail'),
    path('login/', LoginView.as_view(), name='login'),
    path('addFarm/', AddFarm.as_view(), name='add-farm'),
    path('farms/<int:farm_id>/', FarmDetail.as_view(), name='farm-detail'),
    path('users/farms/<int:user_id>', UserFarms.as_view(), name='user-farms'),
    path('addCrop/', AddCrop.as_view(), name='add-crop'),
    path('getFarmCrops/<int:farm_id>', FarmCrops.as_view(), name='farm-crops'),
    path('getCrop/<int:crop_id>', GetCrop.as_view(), name='get-crops'),
    path('addFeedback/', AddFeedback.as_view(), name = 'add-feedback'),
    path('createNotifications/', CreateNotification.as_view(), name = 'create-notification'),
    path('postNotification/', PostNotification.as_view(), name= 'get-crop'),
    path('saveFcmToken/', SaveFcmToken.as_view(), name='save-fcm-token'),
    path('farms/<int:farm_id>/fertility-alerts/', FarmFertilityAlerts.as_view(), name='farm-fertility-alerts'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('sensorData/<int:crop_id>/', CropSensorDataView.as_view(), name='crop-sensor-data'),
    path('feedback/', FeedbackView.as_view(), name='feedback'),
    path('profile/<int:user_id>/', UserProfileView.as_view(), name='user-profile-by-id'),
    path('crops/<int:crop_id>/fertility-recommendations/', CropFertilityRecommendations.as_view(), name='crop_fertility_recommendations'),
    path('getFarmHarvestedCrops/<int:farm_id>', FarmHarvestedCrops.as_view(), name='farm-harvested-crops'),
    path('getFarmWeatherAlerts/<int:farm_id>', FarmWeatherAlerts.as_view(), name='farm-weather-alerts'),
    path('harvestCrop/<int:crop_id>', HarvestCrop.as_view(), name='harvest-crop'),



] 