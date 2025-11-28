
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from django.conf import settings
import os
from .models import Carrera, Facultad, EstadoCronograma, FaseCronograma, Sede, ArchivoCronograma
from .forms import EstadoCronogramaForm, ArchivoCronogramaForm

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('lista_carreras')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def lista_carreras(request):
    sedes = Sede.objects.all().order_by('nombre')
    
    carreras_por_sede = {}
    for sede in sedes:
        carreras_sede = Carrera.objects.filter(sede=sede).select_related('facultad').order_by('facultad__nombre', 'nombre')
        
        facultades_sede = {}
        for carrera in carreras_sede:
            if carrera.facultad.nombre not in facultades_sede:
                facultades_sede[carrera.facultad.nombre] = []
            facultades_sede[carrera.facultad.nombre].append(carrera)
        
        carreras_por_sede[sede] = facultades_sede
    
    context = {
        'carreras_por_sede': carreras_por_sede,
    }
    return render(request, 'lista_carreras.html', context)

@login_required
def detalle_cronograma(request, carrera_id):
    carrera = get_object_or_404(Carrera, id=carrera_id)
    estados = EstadoCronograma.objects.filter(carrera=carrera).select_related('fase')
    
    # Crear estados faltantes si es necesario
    fases_existentes = [estado.fase for estado in estados]
    fases_faltantes = FaseCronograma.objects.exclude(id__in=[f.id for f in fases_existentes])
    
    for fase in fases_faltantes:
        EstadoCronograma.objects.create(carrera=carrera, fase=fase)
    
    estados = EstadoCronograma.objects.filter(carrera=carrera).select_related('fase')
    
    # Calcular progreso general
    total_fases = estados.count()
    fases_completadas = estados.filter(estado='completado').count()
    progreso_porcentaje = (fases_completadas / total_fases * 100) if total_fases > 0 else 0
    
    context = {
        'carrera': carrera,
        'estados': estados,
        'progreso_porcentaje': round(progreso_porcentaje, 1),
        'fases_completadas': fases_completadas,
        'total_fases': total_fases,
    }
    return render(request, 'detalle_cronograma.html', context)

@login_required
def editar_estado_cronograma(request, estado_id):
    estado = get_object_or_404(EstadoCronograma, id=estado_id)
    
    if request.method == 'POST':
        form = EstadoCronogramaForm(request.POST, instance=estado)
        if form.is_valid():
            estado_editado = form.save(commit=False)
            estado_editado.ultimo_editor = request.user
            estado_editado.fecha_actualizacion = timezone.now()
            estado_editado.save()
            
            messages.success(request, f'✅ Estado de {estado.fase.codigo} actualizado correctamente')
            return redirect('detalle_cronograma', carrera_id=estado.carrera.id)
    else:
        form = EstadoCronogramaForm(instance=estado)
    
    context = {
        'estado': estado,
        'form': form,
        'carrera': estado.carrera,
    }
    return render(request, 'editar_estado.html', context)

@login_required
def actualizar_estado_rapido(request, estado_id):
    """Vista para actualización rápida via AJAX"""
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        estado = get_object_or_404(EstadoCronograma, id=estado_id)
        nuevo_estado = request.POST.get('estado')
        
        if nuevo_estado in dict(EstadoCronograma.ESTADOS):
            estado.estado = nuevo_estado
            estado.ultimo_editor = request.user
            estado.fecha_actualizacion = timezone.now()
            
            # Si se marca como completado, establecer fecha de conclusión si no existe
            if nuevo_estado == 'completado' and not estado.fecha_conclusion:
                estado.fecha_conclusion = timezone.now().date()
            
            estado.save()
            
            return JsonResponse({
                'success': True,
                'estado': estado.estado,
                'estado_display': estado.get_estado_display(),
                'fecha_actualizacion': estado.fecha_actualizacion.strftime('%d/%m/%Y %H:%M')
            })
    
    return JsonResponse({'success': False})

@login_required
def gestionar_archivos(request, estado_id):
    """Vista para gestionar archivos de una fase específica"""
    estado = get_object_or_404(EstadoCronograma, id=estado_id)
    archivos = estado.archivos.all()
    
    if request.method == 'POST':
        form = ArchivoCronogramaForm(request.POST, request.FILES)
        if form.is_valid():
            archivo = form.save(commit=False)
            archivo.estado = estado
            archivo.subido_por = request.user
            archivo.save()
            
            messages.success(request, f'✅ Archivo "{archivo.nombre}" subido correctamente')
            return redirect('gestionar_archivos', estado_id=estado_id)
    else:
        form = ArchivoCronogramaForm()
    
    context = {
        'estado': estado,
        'archivos': archivos,
        'form': form,
        'carrera': estado.carrera,
    }
    return render(request, 'gestionar_archivos.html', context)

@login_required
def eliminar_archivo(request, archivo_id):
    """Eliminar un archivo"""
    archivo = get_object_or_404(ArchivoCronograma, id=archivo_id)
    estado_id = archivo.estado.id
    
    # Eliminar archivo físico
    if archivo.archivo:
        if os.path.isfile(archivo.archivo.path):
            os.remove(archivo.archivo.path)
    
    archivo.delete()
    messages.success(request, '✅ Archivo eliminado correctamente')
    return redirect('gestionar_archivos', estado_id=estado_id)

@login_required
def descargar_archivo(request, archivo_id):
    """Descargar un archivo"""
    archivo = get_object_or_404(ArchivoCronograma, id=archivo_id)
    
    if archivo.archivo:
        response = HttpResponse(archivo.archivo, content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{archivo.nombre_archivo()}"'
        return response
    else:
        messages.error(request, '❌ El archivo no existe')
        return redirect('gestionar_archivos', estado_id=archivo.estado.id)