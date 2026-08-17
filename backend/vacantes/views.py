import hashlib
import json
import os

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Evaluacion, PerfilBusqueda, Vacante
from .serializers import (
    EvaluacionSerializer,
    PerfilSerializer,
    VacanteIngestSerializer,
    VacanteListSerializer,
    VacanteSerializer,
)


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


class VacantesListView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request):
        qs = Vacante.objects.all()

        q = request.query_params.get("q")
        if q:
            qs = qs.filter(titulo__icontains=q) | qs.filter(empresa__icontains=q)

        fuente = request.query_params.get("fuente")
        if fuente:
            qs = qs.filter(fuente=fuente)

        try:
            pagina = max(1, int(request.query_params.get("pagina", 1)))
        except ValueError:
            pagina = 1

        tam = 20
        total = qs.count()
        inicio = (pagina - 1) * tam
        resultados = qs[inicio:inicio + tam]

        return Response({
            "total": total,
            "pagina": pagina,
            "paginas": (total + tam - 1) // tam,
            "resultados": VacanteListSerializer(resultados, many=True).data,
        })


class VacanteDetailView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request, pk):
        try:
            vacante = Vacante.objects.get(pk=pk)
        except Vacante.DoesNotExist:
            return Response({"detalle": "No encontrada"}, status=status.HTTP_404_NOT_FOUND)
        return Response(VacanteSerializer(vacante).data)

def _clave_valida(request):
    clave = request.headers.get("X-API-Key")
    return bool(clave) and clave == os.getenv("INGEST_API_KEY")


class PerfilUpsertView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        if not _clave_valida(request):
            return Response({"detalle": "API key invalida"}, status=401)

        datos = json.loads(request.body.decode("utf-8"))
        chat_id = str(datos.get("telegram_chat_id", "")).strip()
        if not chat_id:
            return Response({"detalle": "Falta telegram_chat_id"}, status=400)

        perfil, creado = PerfilBusqueda.objects.get_or_create(
            telegram_chat_id=chat_id,
            defaults={"nombre": datos.get("nombre") or f"Perfil {chat_id}"},
        )

        if datos.get("texto_cv"):
            perfil.texto_cv = datos["texto_cv"][:20000]
        if datos.get("nombre"):
            perfil.nombre = datos["nombre"]
        if datos.get("ubicacion"):
            perfil.ubicacion = datos["ubicacion"]
        if datos.get("palabras_clave"):
            perfil.palabras_clave = datos["palabras_clave"]
        perfil.save()

        return Response({
            "creado": creado,
            "perfil": PerfilSerializer(perfil).data,
            "cv_caracteres": len(perfil.texto_cv),
        }, status=200)


class PendientesEvaluarView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request, chat_id):
        if not _clave_valida(request):
            return Response({"detalle": "API key invalida"}, status=401)

        try:
            perfil = PerfilBusqueda.objects.get(telegram_chat_id=str(chat_id))
        except PerfilBusqueda.DoesNotExist:
            return Response({"detalle": "Perfil no encontrado"}, status=404)

        if not perfil.texto_cv:
            return Response({"detalle": "El perfil no tiene CV cargado"}, status=400)

        evaluadas = Evaluacion.objects.filter(perfil=perfil).values_list("vacante_id", flat=True)
        pendientes = Vacante.objects.exclude(id__in=evaluadas)[:int(request.query_params.get("limite", 10))]

        return Response({
            "perfil_id": perfil.id,
            "texto_cv": perfil.texto_cv,
            "pendientes": [
                {
                    "id": v.id,
                    "titulo": v.titulo,
                    "empresa": v.empresa,
                    "descripcion": v.descripcion[:4000],
                }
                for v in pendientes
            ],
        })


class EvaluacionesIngestView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        if not _clave_valida(request):
            return Response({"detalle": "API key invalida"}, status=401)

        datos = json.loads(request.body.decode("utf-8"))
        items = datos.get("evaluaciones") if isinstance(datos, dict) else datos
        if not isinstance(items, list):
            items = [items]

        guardadas = 0
        for it in items:
            try:
                Evaluacion.objects.update_or_create(
                    vacante_id=it["vacante"],
                    perfil_id=it["perfil"],
                    defaults={
                        "puntuacion": max(0, min(100, int(it.get("puntuacion", 0)))),
                        "razones": it.get("razones", []),
                        "modelo": it.get("modelo", "")[:80],
                    },
                )
                guardadas += 1
            except (KeyError, ValueError, TypeError):
                continue

        return Response({"recibidas": len(items), "guardadas": guardadas}, status=201)


class MejoresView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request, chat_id):
        try:
            perfil = PerfilBusqueda.objects.get(telegram_chat_id=str(chat_id))
        except PerfilBusqueda.DoesNotExist:
            return Response({"detalle": "Perfil no encontrado"}, status=404)

        minimo = int(request.query_params.get("min", 60))
        qs = (Evaluacion.objects
              .filter(perfil=perfil, puntuacion__gte=minimo)
              .select_related("vacante")[:int(request.query_params.get("limite", 10))])

        return Response({
            "total": qs.count(),
            "resultados": EvaluacionSerializer(qs, many=True).data,
        })
