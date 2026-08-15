from django.urls import path

from .views import IngestVacantesView, VacantesListView

urlpatterns = [
    path("vacantes/", VacantesListView.as_view(), name="vacantes-list"),
    path("vacantes/ingest/", IngestVacantesView.as_view(), name="vacantes-ingest"),
]
