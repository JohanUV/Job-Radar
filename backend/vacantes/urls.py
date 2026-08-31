from django.urls import path

from .views import (
    EvaluacionesIngestView,
    IngestVacantesView,
    MejoresView,
    PendientesEvaluarView,
    PerfilUpsertView,
    PostulacionDetailView,
    PostulacionesCreateView,
    PostulacionesListView,
    VacanteDetailView,
    VacantesListView,
    CartaContextoView,
    CartasIngestView
)

urlpatterns = [
    path("vacantes/", VacantesListView.as_view(), name="vacantes-list"),
    path("vacantes/ingest/", IngestVacantesView.as_view(), name="vacantes-ingest"),
    path("vacantes/<int:pk>/", VacanteDetailView.as_view(), name="vacantes-detail"),
    path("perfil/", PerfilUpsertView.as_view(), name="perfil-upsert"),
    path("perfil/<str:chat_id>/pendientes/", PendientesEvaluarView.as_view(), name="perfil-pendientes"),
    path("perfil/<str:chat_id>/mejores/", MejoresView.as_view(), name="perfil-mejores"),
    path("evaluaciones/", EvaluacionesIngestView.as_view(), name="evaluaciones-ingest"),
    path("perfil/<str:chat_id>/carta/<int:vacante_id>/", CartaContextoView.as_view(), name="carta-contexto"),
    path("cartas/", CartasIngestView.as_view(), name="cartas-ingest"),
    path("perfil/<str:chat_id>/postulaciones/", PostulacionesListView.as_view(), name="perfil-postulaciones"),
    path("postulaciones/", PostulacionesCreateView.as_view(), name="postulaciones-create"),
    path("postulaciones/<int:pk>/", PostulacionDetailView.as_view(), name="postulaciones-detail"),
]