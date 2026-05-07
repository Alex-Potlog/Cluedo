from django.core.management.base import BaseCommand

from CasoAbierto.models import Acusado, Arma, Lugar


ACUSADOS = ["Roger", "Jan", "Oscar", "Xavi", "Unai", "Mora"]

LUGARES = [
    "Cocina", "Patio", "Spa", "Teatro", "Clase", "Observatorio",
    "Comedor", "Habitación de invitados", "Vestíbulo",
]

ARMAS = ["Cuerda", "Puñal", "Herramienta", "Pistola", "Candelabro", "Tubería de plomo"]


class Command(BaseCommand):
    help = "Seedea la base de datos con los catálogos del Cluedo."

    def handle(self, *args, **kwargs):
        for nom in ACUSADOS:
            Acusado.objects.get_or_create(nom=nom)
        for nom in LUGARES:
            Lugar.objects.get_or_create(nom=nom)
        for nom in ARMAS:
            Arma.objects.get_or_create(nom=nom)

        self.stdout.write(self.style.SUCCESS("Catàlegs seedats correctament."))
