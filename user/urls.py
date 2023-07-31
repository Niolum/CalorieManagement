from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns

from user.views import RegistryUserView, UserLoginAPIView, UserLogoutAPIView, UserProfileAPIView, UserAPIView



urlpatterns = format_suffix_patterns([
    path('register/', RegistryUserView.as_view(), name='register'),
    path('login/', UserLoginAPIView.as_view(), name='login-user'),
    path('logout/', UserLogoutAPIView.as_view(), name='logout-user'),
    path('user/', UserAPIView.as_view(), name='user-info'),
    path('profile/', UserProfileAPIView.as_view(), name='user-profile')
])