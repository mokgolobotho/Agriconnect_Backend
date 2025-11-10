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
    path('api/farms/<int:farm_id>/fertility-alerts/', FarmFertilityAlerts.as_view(), name='farm-fertility-alerts'),
    path('api/logout/', LogoutView.as_view(), name='logout')

]