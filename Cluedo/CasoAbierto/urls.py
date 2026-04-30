from django.urls import path
from . import views

urlpatterns = [
    # path('', views.mostra_situacio, name='mostra_situacio'),
    path('api/login/', views.api_login, name='api_login'),
    path('api/register/', views.api_register, name='api_register'),
    path('api/csrf/', views.api_csrf, name='api_csrf'),
    path('api/status/', views.api_status, name='api_status'),
    path('api/logout/', views.api_logout, name='api_logout'),
]