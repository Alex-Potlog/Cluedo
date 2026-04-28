from django.contrib import admin
from .models import Acusado, Arma, Lugar, Situacio

# Register your models here.
admin.site.register(Acusado)
admin.site.register(Arma)
admin.site.register(Lugar)
admin.site.register(Situacio)
