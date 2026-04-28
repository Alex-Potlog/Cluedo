from django.shortcuts import render
from .models import Acusado, Arma, Lugar, Situacio

""" def mostra_situacio(request):
    situacio = Situacio.objects.get(pk=1)
    
    # Preparamos los datos para que Vue pueda leerlos fácilmente en formato JSON
    situacio_data = {
        'acusat': situacio.acusado.nom,
        'arma': situacio.arma.nom,
        'lloc': situacio.lugar.nom
    }
    
    return render(request, '', {
        'situacio_data': situacio_data
    }) """