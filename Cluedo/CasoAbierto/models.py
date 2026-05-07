from django.conf import settings
from django.db import models


class Acusado(models.Model):
    nom = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["nom"]
        verbose_name_plural = "Acusados"

    def __str__(self):
        return self.nom


class Arma(models.Model):
    nom = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["nom"]
        verbose_name_plural = "Armas"

    def __str__(self):
        return self.nom


class Lugar(models.Model):
    nom = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["nom"]
        verbose_name_plural = "Lugares"

    def __str__(self):
        return self.nom

class PerfilAgent(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="perfil",
    )
    id_agencia = models.CharField(max_length=20, unique=True)
    data_ingres = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "Perfil d'agent"
        verbose_name_plural = "Perfils d'agents"

    def __str__(self):
        return f"{self.id_agencia} · {self.user.get_username()}"


class Cas(models.Model):
    class Estat(models.TextChoices):
        EN_CURS = "en_curs", "En curs"
        RESOLT = "resolt", "Resolt"
        ARXIVAT = "arxivat", "Arxivat"

    perfil = models.ForeignKey(
        PerfilAgent, on_delete=models.CASCADE, related_name="casos"
    )
    titol = models.CharField(max_length=200, blank=True)
    solucio_acusado = models.ForeignKey(Acusado, on_delete=models.PROTECT)
    solucio_arma = models.ForeignKey(Arma, on_delete=models.PROTECT)
    solucio_lugar = models.ForeignKey(Lugar, on_delete=models.PROTECT)
    intents_max = models.PositiveSmallIntegerField(default=5)
    estat = models.CharField(
        max_length=12, choices=Estat.choices, default=Estat.EN_CURS
    )
    iniciat_el = models.DateTimeField(auto_now_add=True)
    finalitzat_el = models.DateTimeField(null=True, blank=True)
    segons_acumulats = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-iniciat_el"]
        verbose_name = "Cas"
        verbose_name_plural = "Casos"

    def __str__(self):
        return f"Cas #{self.pk:04d}"


class Intent(models.Model):
    class Resultat(models.TextChoices):
        CORRECTE = "correcte", "Correcte"
        PARCIAL = "parcial", "Parcialment correcte"
        INCORRECTE = "incorrecte", "Incorrecte"

    cas = models.ForeignKey(Cas, on_delete=models.CASCADE, related_name="intents")
    numero = models.PositiveSmallIntegerField()
    acusado = models.ForeignKey(Acusado, on_delete=models.PROTECT)
    arma = models.ForeignKey(Arma, on_delete=models.PROTECT)
    lugar = models.ForeignKey(Lugar, on_delete=models.PROTECT)
    resultat = models.CharField(max_length=12, choices=Resultat.choices)
    encerta_acusado = models.BooleanField(default=False)
    encerta_arma = models.BooleanField(default=False)
    encerta_lugar = models.BooleanField(default=False)
    creat_el = models.DateTimeField(auto_now_add=True)
    segons_des_inici = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["cas", "numero"]
        unique_together = [("cas", "numero")]
        verbose_name = "Intent"
        verbose_name_plural = "Intents"

    def __str__(self):
        return f"{self.cas} · intent {self.numero}"
