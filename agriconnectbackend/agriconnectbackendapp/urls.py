from django.urls import path
from .views import *

urlpatterns = [
    path('register/', UserListCreateView.as_view(), name='register'),
    path('users/<str:username>/', UserDetailView.as_view(), name='user-detail'),
    path('login/', LoginView.as_view(), name='login'),
    path('AddFarm/', AddFarm.as_view(), name='AddFarm'),
    path('farms/<int:farm_id>/', FarmDetail.as_view(), name='farm-detail'),
    path('users/farms/<int:user_id>', UserFarms.as_view(), name='user-farms'),
]