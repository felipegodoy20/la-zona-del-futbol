from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# Perfil con RUT, teléfono y rol institucional
class Perfil(models.Model):
    ROL_CHOICES = [
        ('cliente', 'Cliente'),
        ('personal', 'Personal del complejo'),
        ('administrador', 'Administrador'),
    ]

    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    rut = models.CharField(max_length=12, unique=True, null=True, blank=True, verbose_name="RUT")
    telefono = models.CharField(max_length=15, blank=True, verbose_name="Teléfono")
    rol = models.CharField(max_length=20, choices=ROL_CHOICES, default='cliente', verbose_name="Rol institucional")

    class Meta:
        verbose_name_plural = "Perfiles"

    def __str__(self):
        return f"Perfil de {self.usuario.username}"