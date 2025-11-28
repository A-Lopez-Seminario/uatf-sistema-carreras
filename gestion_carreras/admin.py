

from django.contrib import admin
from .models import Facultad, Sede, Carrera, FaseCronograma, EstadoCronograma, ArchivoCronograma

@admin.register(Facultad)
class FacultadAdmin(admin.ModelAdmin):
    list_display = ['nombre']
    search_fields = ['nombre']

@admin.register(Sede)
class SedeAdmin(admin.ModelAdmin):
    list_display = ['nombre']
    search_fields = ['nombre']

@admin.register(Carrera)
class CarreraAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'facultad', 'sede', 'grado_academico']
    list_filter = ['facultad', 'sede', 'grado_academico']
    search_fields = ['nombre', 'facultad__nombre']
    list_per_page = 20

@admin.register(FaseCronograma)
class FaseCronogramaAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'orden']
    list_filter = ['orden']
    search_fields = ['codigo', 'nombre']
    ordering = ['orden']

@admin.register(EstadoCronograma)
class EstadoCronogramaAdmin(admin.ModelAdmin):
    list_display = ['carrera', 'fase', 'estado', 'fecha_actualizacion', 'ultimo_editor']
    list_filter = ['estado', 'fase', 'carrera__facultad']
    search_fields = ['carrera__nombre', 'fase__nombre']
    list_editable = ['estado']
    list_per_page = 20
    readonly_fields = ['fecha_actualizacion', 'ultimo_editor']

@admin.register(ArchivoCronograma)
class ArchivoCronogramaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'estado', 'tipo', 'subido_por', 'fecha_subida']
    list_filter = ['tipo', 'estado__fase', 'estado__carrera__facultad']
    search_fields = ['nombre', 'descripcion', 'estado__carrera__nombre']
    readonly_fields = ['fecha_subida', 'subido_por']
    list_per_page = 20
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Solo para nuevos objetos
            obj.subido_por = request.user
        super().save_model(request, obj, form, change)