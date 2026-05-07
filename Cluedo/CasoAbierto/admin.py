from django.contrib import admin

from .models import (
    Acusado,
    Arma,
    Cas,
    Intent,
    Lugar,
    PerfilAgent,
)


@admin.register(Acusado)
class AcusadoAdmin(admin.ModelAdmin):
    list_display = ("id", "nom")
    search_fields = ("nom",)


@admin.register(Arma)
class ArmaAdmin(admin.ModelAdmin):
    list_display = ("id", "nom")
    search_fields = ("nom",)


@admin.register(Lugar)
class LugarAdmin(admin.ModelAdmin):
    list_display = ("id", "nom")
    search_fields = ("nom",)


@admin.register(PerfilAgent)
class PerfilAgentAdmin(admin.ModelAdmin):
    list_display = ("id_agencia", "user", "data_ingres")
    search_fields = ("id_agencia", "user__username")


class IntentInline(admin.TabularInline):
    model = Intent
    extra = 0
    readonly_fields = ("creat_el",)


@admin.register(Cas)
class CasAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "perfil",
        "estat",
        "iniciat_el",
        "finalitzat_el",
        "segons_acumulats",
    )
    list_filter = ("estat",)
    search_fields = ("perfil__id_agencia",)
    inlines = [IntentInline]


@admin.register(Intent)
class IntentAdmin(admin.ModelAdmin):
    list_display = ("cas", "numero", "resultat", "creat_el")
    list_filter = ("resultat",)
