from django.urls import path

from .views import IngestVacantesView

urlpatterns = [
    path("vacantes/ingest/", IngestVacantesView.as_view(), name="vacantes-ingest"),
]
