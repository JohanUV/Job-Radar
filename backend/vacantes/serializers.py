from rest_framework import serializers

from .models import Evaluacion, PerfilBusqueda, Vacante


class VacanteIngestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacante
        fields = [
            "titulo", "empresa", "descripcion", "ubicacion", "tipo",
            "categoria", "url", "fuente", "fecha_publicacion", "payload",
        ]


class VacanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacante
        fields = "__all__"


class VacanteListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacante
        fields = [
            "id", "titulo", "empresa", "ubicacion", "tipo",
            "categoria", "url", "fuente", "fecha_publicacion",
        ]


class PerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerfilBusqueda
        fields = [
            "id", "nombre", "telegram_chat_id", "palabras_clave",
            "ubicacion", "activo",
        ]


class EvaluacionSerializer(serializers.ModelSerializer):
    titulo = serializers.CharField(source="vacante.titulo", read_only=True)
    empresa = serializers.CharField(source="vacante.empresa", read_only=True)
    url = serializers.CharField(source="vacante.url", read_only=True)
    fuente = serializers.CharField(source="vacante.fuente", read_only=True)
    ubicacion = serializers.CharField(source="vacante.ubicacion", read_only=True)

    class Meta:
        model = Evaluacion
        fields = [
            "id", "vacante", "titulo", "empresa", "ubicacion", "url",
            "fuente", "puntuacion", "razones", "creada",
        ]