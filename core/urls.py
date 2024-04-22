from django.urls import path, include
from core.views import *
from core.views.Autenticate import *

urlpatterns = [
    #path('tipo-usuario/', TipoUsuarioList.as_view()),
    #path('tipo-usuario/<int:pk>/', TipoUsuarioDetail.as_view()),
    #path('carrera/', CarreraList.as_view()),
    #path('carrera/<int:pk>/', CarreraDetail.as_view()),
    #path('carrera/universidad/<int:universidadPK>/', CarreraExtra),
    #path('universidad/', UniversidadList.as_view()),
    #path('universidad/<int:pk>/', UniversidadDetail.as_view()),
    #path('vivienda/', ViviendaList.as_view()),
    #path('vivienda/<int:pk>/', ViviendaDetail.as_view()),
    #path('usuario/', UsuarioList.as_view()),
    #path('usuario/<int:pk>/', UsuarioDetail.as_view()),
    #path('categoria/', CategoriaList.as_view()),
    #path('categoria/<int:pk>/', CategoriaDetail.as_view()),
    #path('entrada/', EntradaList.as_view()),
    #path('entrada/<int:pk>/', EntradaDetail.as_view()),
    #path('bandeja/', BandejaList.as_view()),
    #path('bandeja/<int:pk>/', BandejaDetail.as_view()),
    path('login/', login),
    path('sendEmail/<int:pk>/', sendEmail),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
]
