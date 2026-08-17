import hashlib

from django.conf import settings
from django.db import models


class PerfilBusqueda(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name="perfiles", null=True, blank=True,
    )
    telegram_chat_id = models.CharField(max_length=40, unique=True, null=True, blank=True)
    nombre = models.CharField(max_length=120)
    palabras_clave = models.JSONField(default=list)
    ubicacion = models.CharField(max_length=120, blank=True)
    texto_cv = models.TextField(blank=True)
    activo = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre


class Vacante(models.Model):
    titulo = models.CharField(max_length=255)
    empresa = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)
    ubicacion = models.CharField(max_length=255, blank=True)
    tipo = models.CharField(max_length=80, blank=True, null=True)
    categoria = models.CharField(max_length=120, blank=True, null=True)
    url = models.URLField(max_length=500)
    hash_url = models.CharField(max_length=64, unique=True, editable=False)
    fuente = models.CharField(max_length=50)
    fecha_publicacion = models.DateTimeField(null=True, blank=True)
    capturada = models.DateTimeField(auto_now_add=True)
    payload = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["-capturada"]

    def save(self, *args, **kwargs):
        self.hash_url = hashlib.sha256(self.url.encode()).hexdigest()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.titulo} — {self.empresa}"


class Postulacion(models.Model):
    class Estado(models.TextChoices):
        GUARDADA = "guardada", "Guardada"
        POSTULADA = "postulada", "Postulada"
        ENTREVISTA = "entrevista", "Entrevista"
        CERRADA = "cerrada", "Cerrada"

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="postulaciones")
    vacante = models.ForeignKey(Vacante, on_delete=models.CASCADE, related_name="postulaciones")
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.GUARDADA)
    notas = models.TextField(blank=True)
    creada = models.DateTimeField(auto_now_add=True)
    actualizada = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("usuario", "vacante")
        ordering = ["-actualizada"]

    def __str__(self):
        return f"{self.vacante.titulo} [{self.get_estado_display()}]"


class HistorialEstado(models.Model):
    postulacion = models.ForeignKey(Postulacion, on_delete=models.CASCADE, related_name="historial")
    estado_anterior = models.CharField(max_length=20, blank=True)
    estado_nuevo = models.CharField(max_length=20)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-fecha"]


class Evaluacion(models.Model):
    vacante = models.ForeignKey(Vacante, on_delete=models.CASCADE, related_name="evaluaciones")
    perfil = models.ForeignKey(PerfilBusqueda, on_delete=models.CASCADE, related_name="evaluaciones")
    puntuacion = models.IntegerField()
    razones = models.JSONField(default=list)
    modelo = models.CharField(max_length=80, blank=True)
    creada = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("vacante", "perfil")
        ordering = ["-puntuacion"]

    def __str__(self):
        return f"{self.vacante.titulo}: {self.puntuacion}"
        