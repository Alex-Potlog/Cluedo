from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
import json

from account.models import Account

from .models import Acusado, Arma, Lugar, Situacio

@require_GET
@ensure_csrf_cookie
def api_csrf(request):
    return JsonResponse({'message': 'CSRF cookie set'})

@csrf_exempt
@require_POST
def api_login(request):
    try:
        data = json.loads(request.body)
        login_id = data.get('email')  # Aquest camp ve del form de Vue (pot ser email o username)
        password = data.get('password')
        
        # Intentem buscar l'usuari per email primer, si no, assumim que és un username
        try:
            user_obj = User.objects.get(email=login_id)
            auth_username = user_obj.username
        except User.DoesNotExist:
            auth_username = login_id
            
        user = authenticate(request, username=auth_username, password=password)
        if user is not None:
            auth_login(request, user)
            return JsonResponse({'success': True, 'message': 'Sessió iniciada correctament.'})
        else:
            return JsonResponse({'success': False, 'message': 'Correu o contrasenya incorrectes.'}, status=400)
    except Exception as e:
        print(f"Error en login: {str(e)}")
        return JsonResponse({'success': False, 'message': "S'ha produït un error al servidor."}, status=500)

@csrf_exempt
@require_POST
def api_register(request):
    try:
        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not username or not email or not password:
            return JsonResponse({'success': False, 'message': 'Tots els camps són obligatoris (Usuari, Email i Contrasenya).'}, status=400)

        if len(password) < 8:
            return JsonResponse({'success': False, 'message': 'La contrasenya ha de tenir almenys 8 caràcters.'}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({'success': False, 'message': "Aquest nom d'usuari ja està registrat."}, status=400)
            
        if User.objects.filter(email=email).exists():
            return JsonResponse({'success': False, 'message': 'Aquest correu electrònic ja està en ús.'}, status=400)

        # Creem l'usuari (el model Account es crea automàticament per un senyal de django-user-accounts)
        user = User.objects.create_user(username=username, email=email, password=password)
        
        auth_login(request, user)
        return JsonResponse({'success': True, 'message': 'Benvingut! Compte creat correctament.'})
    except Exception as e:
        # Per a errors inesperats, enviem un missatge més net a l'usuari però loguegem l'error real
        print(f"Error en registre: {str(e)}")
        return JsonResponse({'success': False, 'message': "S'ha produït un error en processar el registre. Torna-ho a intentar més tard."}, status=500)

@require_GET
def api_status(request):
    if request.user.is_authenticated:
        return JsonResponse({
            'is_authenticated': True,
            'username': request.user.username
        })
    return JsonResponse({'is_authenticated': False})

@require_POST
@csrf_exempt
def api_logout(request):
    from django.contrib.auth import logout as auth_logout
    auth_logout(request)
    return JsonResponse({'success': True, 'message': 'Sessió tancada correctament.'})