from django.urls import path, include

urlpatterns = [
    path('api/', include('locations.urls')),
    path('api/', include('accounts.urls')),
    path('api/', include('studies.urls')),
    path('api/', include('socials.urls')),
    path('api/', include('payments.urls'))
]
