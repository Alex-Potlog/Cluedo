from django.db import models

class Acusado(models.Model):
    nom = models.CharField(max_length=255)

class Lugar(models.Model):
    nom = models.CharField(max_length=255)

class Arma(models.Model):
    nom = models.CharField(max_length=255)

class Situacio(models.Model):
    acusado = models.ForeignKey(Acusado, on_delete=models.CASCADE)
    arma = models.ForeignKey(Arma, on_delete=models.CASCADE)
    lugar = models.ForeignKey(Lugar, on_delete=models.CASCADE)