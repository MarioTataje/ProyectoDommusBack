from django.urls import path

from .views import register_user, user_detail, self_personality_detail, target_personality_detail, contacts_list

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='login_token'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', register_user, name='register_user'),
    path('users/<int:user_id>/', user_detail, name='user_detail'),
    path('users/<int:user_id>/self-personalities/', self_personality_detail, name='self_personality_detail'),
    path('users/<int:user_id>/target-personalities/', target_personality_detail, name='target_personality_detail'),
    path('users/<int:user_id>/contacts/', contacts_list, name='contacts_list')
]
