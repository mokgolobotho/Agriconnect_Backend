from django.urls import path
from .views import UserListCreateView, UserDetailView

urlpatterns = [
    path('register/', UserListCreateView.as_view(), name='register'),
    path('users/<str:username>/', UserDetailView.as_view(), name='user-detail'),
]