from rest_framework import serializers

from .models import Vacante


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
