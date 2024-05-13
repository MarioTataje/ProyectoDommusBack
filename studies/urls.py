from django.urls import path
from .views import universities_list, degrees_list


urlpatterns = [
    path('universities/', universities_list, name='universities_list'),
    path('universities/<int:university_id>/degrees/', degrees_list, name='degrees_list')
]