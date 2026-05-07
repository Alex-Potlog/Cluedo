import json
import random
import secrets

from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from .models import Acusado, Arma, Cas, Intent, Lugar, PerfilAgent


# ---------- Auth ----------

@require_GET
@ensure_csrf_cookie
def api_csrf(request):
    return JsonResponse({'message': 'CSRF cookie set'})


@csrf_exempt
@require_POST
def api_login(request):
    try:
        data = json.loads(request.body)
        login_id = data.get('email')
        password = data.get('password')

        try:
            user_obj = User.objects.get(email=login_id)
            auth_username = user_obj.username
        except User.DoesNotExist:
            auth_username = login_id

        user = authenticate(request, username=auth_username, password=password)
        if user is not None:
            auth_login(request, user)
            return JsonResponse({'success': True, 'message': 'Sessió iniciada correctament.'})
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

        user = User.objects.create_user(username=username, email=email, password=password)
        auth_login(request, user)
        return JsonResponse({'success': True, 'message': 'Benvingut! Compte creat correctament.'})
    except Exception as e:
        print(f"Error en registre: {str(e)}")
        return JsonResponse({'success': False, 'message': "S'ha produït un error en processar el registre. Torna-ho a intentar més tard."}, status=500)


@require_GET
def api_status(request):
    if request.user.is_authenticated:
        return JsonResponse({
            'is_authenticated': True,
            'username': request.user.username,
        })
    return JsonResponse({'is_authenticated': False})


@require_POST
@csrf_exempt
def api_logout(request):
    auth_logout(request)
    return JsonResponse({'success': True, 'message': 'Sessió tancada correctament.'})


# ---------- Game ----------

def _get_or_create_perfil(user):
    perfil = PerfilAgent.objects.filter(user=user).first()
    if perfil:
        return perfil
    while True:
        codi = f"AGT-{secrets.randbelow(100000):05d}"
        if not PerfilAgent.objects.filter(id_agencia=codi).exists():
            return PerfilAgent.objects.create(user=user, id_agencia=codi)


def _serialize_intent(intent):
    return {
        'numero': intent.numero,
        'acusado': intent.acusado.nom,
        'arma': intent.arma.nom,
        'lugar': intent.lugar.nom,
        'resultat': intent.resultat,
        'encerta_acusado': intent.encerta_acusado,
        'encerta_arma': intent.encerta_arma,
        'encerta_lugar': intent.encerta_lugar,
        'creat_el': intent.creat_el.isoformat(),
        'segons_des_inici': intent.segons_des_inici,
    }


def _serialize_cas(cas, include_intents=True, include_solucio=False):
    data = {
        'id': cas.id,
        'titol': cas.titol or f"Cas #{cas.pk:04d}",
        'estat': cas.estat,
        'intents_max': cas.intents_max,
        'intents_usats': cas.intents.count(),
        'iniciat_el': cas.iniciat_el.isoformat(),
        'finalitzat_el': cas.finalitzat_el.isoformat() if cas.finalitzat_el else None,
        'segons_acumulats': cas.segons_acumulats,
    }
    if include_intents:
        data['intents'] = [_serialize_intent(i) for i in cas.intents.all().order_by('-numero')]
    if include_solucio:
        data['solucio'] = {
            'acusado': cas.solucio_acusado.nom,
            'arma': cas.solucio_arma.nom,
            'lugar': cas.solucio_lugar.nom,
        }
    return data


@require_GET
def api_catalog(request):
    return JsonResponse({
        'acusados': list(Acusado.objects.values('id', 'nom')),
        'armas': list(Arma.objects.values('id', 'nom')),
        'lugares': list(Lugar.objects.values('id', 'nom')),
    })


# ---------- Endpoints amb noms de l'enunciat ----------

@require_GET
def api_personatges(request):
    """Llista de personatges (sospitosos). Wrapper sobre Acusado."""
    return JsonResponse({
        'personatges': list(Acusado.objects.values('id', 'nom')),
    })


@require_GET
def api_armes(request):
    """Llista d'armes."""
    return JsonResponse({
        'armes': list(Arma.objects.values('id', 'nom')),
    })


@require_GET
def api_habitacions(request):
    """Llista d'habitacions. Wrapper sobre Lugar."""
    return JsonResponse({
        'habitacions': list(Lugar.objects.values('id', 'nom')),
    })


@csrf_exempt
@require_POST
def api_acusar(request):
    """
    Endpoint d'acusació segons l'enunciat.
    Rep {acusado_id, arma_id, lugar_id} (o els alies personatge_id / habitacio_id),
    busca el cas en curs de l'usuari (en crea un si no en té) i delega
    a la mateixa lògica que api_cas_intent.
    """
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'message': 'Cal iniciar sessió.'}, status=401)

    perfil = _get_or_create_perfil(request.user)

    try:
        data = json.loads(request.body)
        acusado_id = data.get('acusado_id') or data.get('personatge_id')
        arma_id = data.get('arma_id')
        lugar_id = data.get('lugar_id') or data.get('habitacio_id')
        if acusado_id is None or arma_id is None or lugar_id is None:
            raise KeyError
        acusado = Acusado.objects.get(pk=acusado_id)
        arma = Arma.objects.get(pk=arma_id)
        lugar = Lugar.objects.get(pk=lugar_id)
    except (KeyError, ValueError, TypeError, json.JSONDecodeError):
        return JsonResponse({'success': False, 'message': 'Petició mal formada.'}, status=400)
    except (Acusado.DoesNotExist, Arma.DoesNotExist, Lugar.DoesNotExist):
        return JsonResponse({'success': False, 'message': 'Selecció no vàlida.'}, status=400)

    cas = perfil.casos.filter(estat=Cas.Estat.EN_CURS).order_by('-iniciat_el').first()
    if cas is None:
        # Crear automàticament un nou cas si no n'hi ha cap d'actiu.
        acusados = list(Acusado.objects.all())
        armas = list(Arma.objects.all())
        lugares = list(Lugar.objects.all())
        if not (acusados and armas and lugares):
            return JsonResponse(
                {'success': False, 'message': "Catàleg buit. Executa 'manage.py seed'."},
                status=500,
            )
        cas = Cas.objects.create(
            perfil=perfil,
            solucio_acusado=random.choice(acusados),
            solucio_arma=random.choice(armas),
            solucio_lugar=random.choice(lugares),
        )

    encerta_acusado = acusado.id == cas.solucio_acusado_id
    encerta_arma = arma.id == cas.solucio_arma_id
    encerta_lugar = lugar.id == cas.solucio_lugar_id

    if encerta_acusado and encerta_arma and encerta_lugar:
        resultat = Intent.Resultat.CORRECTE
    elif encerta_acusado or encerta_arma or encerta_lugar:
        resultat = Intent.Resultat.PARCIAL
    else:
        resultat = Intent.Resultat.INCORRECTE

    numero = cas.intents.count() + 1
    segons = int((timezone.now() - cas.iniciat_el).total_seconds())
    intent = Intent.objects.create(
        cas=cas,
        numero=numero,
        acusado=acusado,
        arma=arma,
        lugar=lugar,
        resultat=resultat,
        encerta_acusado=encerta_acusado,
        encerta_arma=encerta_arma,
        encerta_lugar=encerta_lugar,
        segons_des_inici=segons,
    )

    cas_tancat = False
    if resultat == Intent.Resultat.CORRECTE:
        cas.estat = Cas.Estat.RESOLT
        cas.finalitzat_el = timezone.now()
        cas.segons_acumulats = segons
        cas.save()
        cas_tancat = True
    elif numero >= cas.intents_max:
        cas.estat = Cas.Estat.ARXIVAT
        cas.finalitzat_el = timezone.now()
        cas.segons_acumulats = segons
        cas.save()
        cas_tancat = True

    return JsonResponse({
        'success': True,
        'intent': _serialize_intent(intent),
        'cas': _serialize_cas(cas, include_solucio=cas_tancat),
        'cas_tancat': cas_tancat,
    })


@require_GET
def api_cas_active(request):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'message': 'Cal iniciar sessió.'}, status=401)

    perfil = _get_or_create_perfil(request.user)
    cas = perfil.casos.filter(estat=Cas.Estat.EN_CURS).order_by('-iniciat_el').first()
    if not cas:
        return JsonResponse({'success': True, 'cas': None})
    return JsonResponse({'success': True, 'cas': _serialize_cas(cas)})


@csrf_exempt
@require_POST
def api_cas_new(request):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'message': 'Cal iniciar sessió.'}, status=401)

    perfil = _get_or_create_perfil(request.user)

    if perfil.casos.filter(estat=Cas.Estat.EN_CURS).exists():
        return JsonResponse({'success': False, 'message': 'Ja tens un cas en curs.'}, status=400)

    acusados = list(Acusado.objects.all())
    armas = list(Arma.objects.all())
    lugares = list(Lugar.objects.all())
    if not (acusados and armas and lugares):
        return JsonResponse({'success': False, 'message': "Catàleg buit. Executa 'manage.py seed'."}, status=500)

    cas = Cas.objects.create(
        perfil=perfil,
        solucio_acusado=random.choice(acusados),
        solucio_arma=random.choice(armas),
        solucio_lugar=random.choice(lugares),
    )
    return JsonResponse({'success': True, 'cas': _serialize_cas(cas)})


@csrf_exempt
@require_POST
def api_cas_intent(request, cas_id):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'message': 'Cal iniciar sessió.'}, status=401)

    perfil = _get_or_create_perfil(request.user)
    try:
        cas = Cas.objects.get(pk=cas_id, perfil=perfil)
    except Cas.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Cas no trobat.'}, status=404)

    if cas.estat != Cas.Estat.EN_CURS:
        return JsonResponse({'success': False, 'message': 'Aquest cas ja està tancat.'}, status=400)

    try:
        data = json.loads(request.body)
        acusado = Acusado.objects.get(pk=data['acusado_id'])
        arma = Arma.objects.get(pk=data['arma_id'])
        lugar = Lugar.objects.get(pk=data['lugar_id'])
    except (KeyError, ValueError, json.JSONDecodeError):
        return JsonResponse({'success': False, 'message': 'Petició mal formada.'}, status=400)
    except (Acusado.DoesNotExist, Arma.DoesNotExist, Lugar.DoesNotExist):
        return JsonResponse({'success': False, 'message': 'Selecció no vàlida.'}, status=400)

    encerta_acusado = acusado.id == cas.solucio_acusado_id
    encerta_arma = arma.id == cas.solucio_arma_id
    encerta_lugar = lugar.id == cas.solucio_lugar_id

    if encerta_acusado and encerta_arma and encerta_lugar:
        resultat = Intent.Resultat.CORRECTE
    elif encerta_acusado or encerta_arma or encerta_lugar:
        resultat = Intent.Resultat.PARCIAL
    else:
        resultat = Intent.Resultat.INCORRECTE

    numero = cas.intents.count() + 1
    segons = int((timezone.now() - cas.iniciat_el).total_seconds())
    intent = Intent.objects.create(
        cas=cas,
        numero=numero,
        acusado=acusado,
        arma=arma,
        lugar=lugar,
        resultat=resultat,
        encerta_acusado=encerta_acusado,
        encerta_arma=encerta_arma,
        encerta_lugar=encerta_lugar,
        segons_des_inici=segons,
    )

    cas_tancat = False
    if resultat == Intent.Resultat.CORRECTE:
        cas.estat = Cas.Estat.RESOLT
        cas.finalitzat_el = timezone.now()
        cas.segons_acumulats = segons
        cas.save()
        cas_tancat = True
    elif numero >= cas.intents_max:
        cas.estat = Cas.Estat.ARXIVAT
        cas.finalitzat_el = timezone.now()
        cas.segons_acumulats = segons
        cas.save()
        cas_tancat = True

    response = {
        'success': True,
        'intent': _serialize_intent(intent),
        'cas': _serialize_cas(cas, include_solucio=cas_tancat),
        'cas_tancat': cas_tancat,
    }
    return JsonResponse(response)


@require_GET
def api_cas_history(request):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'message': 'Cal iniciar sessió.'}, status=401)

    perfil = _get_or_create_perfil(request.user)
    casos = perfil.casos.exclude(estat=Cas.Estat.EN_CURS).order_by('-finalitzat_el')[:20]
    return JsonResponse({
        'success': True,
        'perfil': {
            'id_agencia': perfil.id_agencia,
            'data_ingres': perfil.data_ingres.isoformat(),
        },
        'casos': [_serialize_cas(c, include_intents=False, include_solucio=True) for c in casos],
    })
