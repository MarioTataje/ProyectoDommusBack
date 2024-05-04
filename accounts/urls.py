from django.urls import path

from .views import register_user, user_detail

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='login_token'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', register_user, name='register_user'),
    path('users/<int:user_id>/', user_detail, name='user_detail')
]
