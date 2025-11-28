
from django.core.management.base import BaseCommand
from gestion_carreras.models import Facultad, Sede, Carrera, FaseCronograma

class Command(BaseCommand):
    help = 'Carga los datos iniciales de facultades, sedes y carreras'
    
    def handle(self, *args, **kwargs):
        # Crear sedes
        sedes_data = ['Potosí', 'Villazón', 'Tupiza', 'Uyuni', 'Uncía', 'Llica']
        sedes = {}
        for sede_nombre in sedes_data:
            sede, created = Sede.objects.get_or_create(nombre=sede_nombre)
            sedes[sede_nombre] = sede
            self.stdout.write(f"Sede {'creada' if created else 'existente'}: {sede_nombre}")
        
        # Crear fases del cronograma
        fases_data = [
            ('RC', 'Organización en Comisión de Rediseño Curricular'),
            ('PC', 'Recolección de Documentos y Proyecto Curricular'),
            ('DI', 'Diagnóstico Inicial de la Carrera'),
            ('EC', 'Estudio de Contexto'),
            ('MM', 'Mesa Multisectorial'),
            ('MC', 'Elaboración de la Propuesta Macro Curricular'),
            ('RAC', 'Reunión Académica de Carrera'),
            ('VT', 'Validación Técnica'),
            ('VN', 'Validación Normativa'),
            ('CA', 'Comisión Académica'),
            ('HCU', 'Honorable Consejo Universitario'),
            ('RAN', 'Reunión Académica Nacional'),
        ]
        
        for codigo, nombre in fases_data:
            fase, created = FaseCronograma.objects.get_or_create(
                codigo=codigo, 
                nombre=nombre
            )
            self.stdout.write(f"Fase {'creada' if created else 'existente'}: {codigo}")
        
        self.stdout.write(self.style.SUCCESS('Datos iniciales cargados exitosamente'))