from django.urls import path
from . import views

urlpatterns = [
    path('api/login/', views.api_login, name='api_login'),
    path('api/register/', views.api_register, name='api_register'),
    path('api/csrf/', views.api_csrf, name='api_csrf'),
    path('api/status/', views.api_status, name='api_status'),
    path('api/logout/', views.api_logout, name='api_logout'),

    path('api/catalog/', views.api_catalog, name='api_catalog'),
    path('api/cas/active/', views.api_cas_active, name='api_cas_active'),
    path('api/cas/new/', views.api_cas_new, name='api_cas_new'),
    path('api/cas/<int:cas_id>/intent/', views.api_cas_intent, name='api_cas_intent'),
    path('api/cas/history/', views.api_cas_history, name='api_cas_history'),

    path('api/personatges/', views.api_personatges, name='api_personatges'),
    path('api/armes/', views.api_armes, name='api_armes'),
    path('api/habitacions/', views.api_habitacions, name='api_habitacions'),
    path('api/acusar/', views.api_acusar, name='api_acusar'),
]
