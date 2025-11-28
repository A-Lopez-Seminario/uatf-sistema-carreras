
from django.db import models
from django.contrib.auth.models import User
import os

def archivo_upload_path(instance, filename):
    """Genera ruta para guardar archivos: carrera_id/fase/filename"""
    carrera_id = instance.estado.carrera.id
    fase_codigo = instance.estado.fase.codigo
    return f'carrera_{carrera_id}/{fase_codigo}/{filename}'

class Facultad(models.Model):
    nombre = models.CharField(max_length=200)
    
    def __str__(self):
        return self.nombre

class Sede(models.Model):
    nombre = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre

class Carrera(models.Model):
    TIPO_GRADO = [
        ('licenciatura', 'Licenciatura'),
        ('tecnico_superior', 'Técnico Superior'),
        ('tecnico_medio', 'Técnico Universitario Medio'),
    ]
    
    facultad = models.ForeignKey(Facultad, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200)
    sede = models.ForeignKey(Sede, on_delete=models.CASCADE)
    grado_academico = models.CharField(max_length=20, choices=TIPO_GRADO, default='licenciatura')
    diploma_academico = models.CharField(max_length=300, blank=True)
    tiempo_estudios = models.CharField(max_length=100, blank=True)
    titulo_provision_nacional = models.CharField(max_length=300, blank=True)
    
    def __str__(self):
        return f"{self.nombre} - {self.sede}"

class FaseCronograma(models.Model):
    nombre = models.CharField(max_length=200)
    codigo = models.CharField(max_length=10)
    descripcion = models.TextField(blank=True)
    orden = models.IntegerField(default=0)
    medios_verificacion = models.TextField(blank=True, help_text="Medios de verificación esperados")
    
    class Meta:
        ordering = ['orden']
        verbose_name = "Fase del Cronograma"
        verbose_name_plural = "Fases del Cronograma"
    
    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

class EstadoCronograma(models.Model):
    ESTADOS = [
        ('pendiente', '⏳ Pendiente'),
        ('en_proceso', '🔄 En Proceso'),
        ('completado', '✅ Completado'),
    ]
    
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE)
    fase = models.ForeignKey(FaseCronograma, on_delete=models.CASCADE)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_conclusion = models.DateField(null=True, blank=True)
    medios_verificacion = models.TextField(blank=True, help_text="Medios de verificación cumplidos")
    observaciones = models.TextField(blank=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    ultimo_editor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        unique_together = ['carrera', 'fase']
        ordering = ['fase__orden']
        verbose_name = "Estado del Cronograma"
        verbose_name_plural = "Estados del Cronograma"
    
    def __str__(self):
        return f"{self.carrera} - {self.fase}: {self.estado}"
    
    def tiene_archivos(self):
        return self.archivos.exists()

class ArchivoCronograma(models.Model):
    TIPOS_ARCHIVO = [
        ('documento', 'Documento'),
        ('acta', 'Acta'),
        ('resolucion', 'Resolución'),
        ('informe', 'Informe'),
        ('otro', 'Otro'),
    ]
    
    estado = models.ForeignKey(EstadoCronograma, on_delete=models.CASCADE, related_name='archivos')
    archivo = models.FileField(upload_to=archivo_upload_path, verbose_name="Archivo")
    tipo = models.CharField(max_length=20, choices=TIPOS_ARCHIVO, default='documento')
    nombre = models.CharField(max_length=200, help_text="Nombre descriptivo del archivo")
    descripcion = models.TextField(blank=True, help_text="Descripción del contenido del archivo")
    fecha_subida = models.DateTimeField(auto_now_add=True)
    subido_por = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = "Archivo del Cronograma"
        verbose_name_plural = "Archivos del Cronograma"
        ordering = ['-fecha_subida']
    
    def __str__(self):
        return f"{self.nombre} - {self.estado.fase.codigo}"
    
    def nombre_archivo(self):
        return os.path.basename(self.archivo.name)
    
    def extension(self):
        return os.path.splitext(self.archivo.name)[1].lower()
    
    def es_pdf(self):
        return self.extension() == '.pdf'
    
    def es_word(self):
        return self.extension() in ['.doc', '.docx']