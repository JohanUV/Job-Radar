import hashlib
import json
import os

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Vacante
from .serializers import VacanteIngestSerializer


def _extraer_lista(data):
    if isinstance(data, str):
        data = json.loads(data)
    if isinstance(data, dict):
        if "vacantes" in data:
            return _extraer_lista(data["vacantes"])
        return [data]
    if isinstance(data, list):
        return data
    return []


class IngestVacantesView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        clave = request.headers.get("X-API-Key")
        if not clave or clave != os.getenv("INGEST_API_KEY"):
            return Response(
                {"detalle": "API key invalida o ausente"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            crudo = request.body.decode("utf-8").strip()
            datos = _extraer_lista(json.loads(crudo))
        except Exception:
            return Response(
                {"detalle": "El cuerpo no es JSON valido"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not datos:
            return Response(
                {"detalle": "No se recibieron vacantes"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = VacanteIngestSerializer(data=datos, many=True)
        serializer.is_valid(raise_exception=True)

        creadas = 0
        duplicadas = 0

        for item in serializer.validated_data:
            huella = hashlib.sha256(item["url"].encode()).hexdigest()
            if Vacante.objects.filter(hash_url=huella).exists():
                duplicadas += 1
                continue
            Vacante.objects.create(**item)
            creadas += 1

        return Response(
            {"recibidas": len(datos), "creadas": creadas, "duplicadas": duplicadas},
            status=status.HTTP_201_CREATED,
        )
