
from django.core.management.base import BaseCommand
from gestion_carreras.models import FaseCronograma

class Command(BaseCommand):
    help = 'Carga las fases del cronograma según el documento oficial'
    
    def handle(self, *args, **kwargs):
        fases_data = [
            (1, 'RC', 'Organización en Comisión de Rediseño Curricular "RC"', 
             'Dictamen Consejo de Carrera. Nómina de integrantes'),
            
            (2, 'PC', 'Recolección de Documentos y Proyecto Curricular "PC"', 
             'Disponibilidad de documentos. Proyecto Curricular y otros.'),
            
            (3, 'DI', 'Diagnóstico Inicial de la Carrera "DI"', 
             'Documento entregado al Dpto. Gestión Curricular.'),
            
            (4, 'EC', 'Estudio de Contexto "EC"', 
             'Documento entregado al Dpto. Gestión Curricular.'),
            
            (5, 'MM', 'Mesa Multisectorial "MM"', 
             'Programas, invitaciones Actas firmadas (fotos)'),
            
            (6, 'MC', 'Elaboración de la Propuesta Macro Curricular "MC"', 
             'Documento borrador revisado listo para la RAC'),
            
            (7, 'RAC', 'Reunión Académica de Carrera "RAC"', 
             'Convocatoria, reglamento, programa, actas firmadas.'),
            
            (8, 'VT', 'Validación Técnica (Dpto. Gestión Curricular) "VT"', 
             'Documento (carta) revisado y entregado a la DSA.'),
            
            (9, 'VN', 'Validación Normativa (Dirección Servicios Académicos) "VN"', 
             'Documento preparado para la "CA".'),
            
            (10, 'CA', 'Comisión Académica "CA"', 
             'Dictamen emanado para su homologación por el "HCU"'),
            
            (11, 'HCU', 'Honorable Consejo Universitario "HCU"', 
             'Resolución del "HCU" para adjuntar al documento de RC.'),
            
            (12, 'RAN', 'Reunión Académica Nacional "RAN"', 
             'Resolución de aprobación del Rediseño Curricular.'),
        ]
        
        for orden, codigo, nombre, medios in fases_data:
            fase, created = FaseCronograma.objects.get_or_create(
                codigo=codigo,
                defaults={
                    'nombre': nombre,
                    'orden': orden,
                    'medios_verificacion': medios
                }
            )
            if created:
                self.stdout.write(f"✅ Fase creada: {codigo} - {nombre}")
            else:
                self.stdout.write(f"📝 Fase existente: {codigo} - {nombre}")
        
        self.stdout.write(self.style.SUCCESS('🎯 Todas las fases del cronograma han sido cargadas!'))