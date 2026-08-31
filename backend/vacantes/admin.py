from django.contrib import admin

from .models import HistorialEstado, PerfilBusqueda, Postulacion, Vacante


@admin.register(Vacante)
class VacanteAdmin(admin.ModelAdmin):
    list_display = ("titulo", "empresa", "ubicacion", "fuente", "capturada")
    list_filter = ("fuente", "categoria", "tipo")
    search_fields = ("titulo", "empresa", "descripcion")
    readonly_fields = ("hash_url", "capturada")


@admin.register(PerfilBusqueda)
class PerfilBusquedaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "usuario", "activo", "creado")
    list_filter = ("activo",)


@admin.register(Postulacion)
class PostulacionAdmin(admin.ModelAdmin):
    list_display = ("vacante", "perfil", "estado", "actualizada")
    list_filter = ("estado",)
    search_fields = ("vacante__titulo", "vacante__empresa")


@admin.register(HistorialEstado)
class HistorialEstadoAdmin(admin.ModelAdmin):
    list_display = ("postulacion", "estado_anterior", "estado_nuevo", "fecha")
