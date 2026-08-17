from django.urls import path

from .views import (
    EvaluacionesIngestView,
    IngestVacantesView,
    MejoresView,
    PendientesEvaluarView,
    PerfilUpsertView,
    VacanteDetailView,
    VacantesListView,
)

urlpatterns = [
    path("vacantes/", VacantesListView.as_view(), name="vacantes-list"),
    path("vacantes/ingest/", IngestVacantesView.as_view(), name="vacantes-ingest"),
    path("vacantes/<int:pk>/", VacanteDetailView.as_view(), name="vacantes-detail"),
    path("perfil/", PerfilUpsertView.as_view(), name="perfil-upsert"),
    path("perfil/<str:chat_id>/pendientes/", PendientesEvaluarView.as_view(), name="perfil-pendientes"),
    path("perfil/<str:chat_id>/mejores/", MejoresView.as_view(), name="perfil-mejores"),
    path("evaluaciones/", EvaluacionesIngestView.as_view(), name="evaluaciones-ingest"),
]