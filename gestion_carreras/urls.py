
from django.urls import path
from . import views
from .reportes import reporte_pdf_carrera, reporte_excel_carrera

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('carreras/', views.lista_carreras, name='lista_carreras'),
    path('cronograma/<int:carrera_id>/', views.detalle_cronograma, name='detalle_cronograma'),
    path('editar-estado/<int:estado_id>/', views.editar_estado_cronograma, name='editar_estado'),
    path('actualizar-estado-rapido/<int:estado_id>/', views.actualizar_estado_rapido, name='actualizar_estado_rapido'),
    # Reportes
    path('reporte/pdf/<int:carrera_id>/', reporte_pdf_carrera, name='reporte_pdf'),
    path('reporte/excel/<int:carrera_id>/', reporte_excel_carrera, name='reporte_excel'),
    # Archivos
    path('archivos/<int:estado_id>/', views.gestionar_archivos, name='gestionar_archivos'),
    path('archivos/eliminar/<int:archivo_id>/', views.eliminar_archivo, name='eliminar_archivo'),
    path('archivos/descargar/<int:archivo_id>/', views.descargar_archivo, name='descargar_archivo'),
]