from django.urls import path
from .views import plans_list, user_plan


urlpatterns = [
    path('plans/', plans_list, name='plans_list'),
    path('users/<int:user_id>/plans/', user_plan, name='user_plan')
]