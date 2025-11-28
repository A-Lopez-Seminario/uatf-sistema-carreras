
from django.core.management.base import BaseCommand
from gestion_carreras.models import Facultad, Sede, Carrera, FaseCronograma

class Command(BaseCommand):
    help = 'Carga TODAS las carreras de la UATF según el documento oficial'
    
    def handle(self, *args, **kwargs):
        self.crear_sedes()
        self.crear_facultades()
        self.crear_fases_cronograma()
        self.crear_carreras_potosi()
        self.crear_carreras_sedes_regionales()
        
        self.stdout.write(self.style.SUCCESS('✅ TODAS las carreras han sido cargadas exitosamente!'))
    
    def crear_sedes(self):
        sedes_data = [
            'Potosí', 'Villazón', 'Tupiza', 'Uyuni', 'Uncía', 'Llica', 
            'San Cristóbal', 'Río Grande'
        ]
        
        for sede_nombre in sedes_data:
            Sede.objects.get_or_create(nombre=sede_nombre)
            self.stdout.write(f"Sede: {sede_nombre}")
    
    def crear_facultades(self):
        facultades_data = [
            'Facultad de Artes',
            'Facultad de Ciencias Agrícolas y Pecuarias',
            'Facultad de Ciencias Económicas, Financieras y Administrativas',
            'Facultad de Ciencias Puras',
            'Facultad de Ciencias Sociales y Humanísticas',
            'Facultad de Derecho',
            'Facultad de Ingeniería',
            'Facultad de Ingeniería Geológica',
            'Facultad de Ingeniería Minera',
            'Facultad de Ingeniería Tecnológica',
            'Facultad de Ciencias de la Salud',
            'Facultad de Medicina',
            'Vicerrectorado'
        ]
        
        for facultad_nombre in facultades_data:
            Facultad.objects.get_or_create(nombre=facultad_nombre)
            self.stdout.write(f"Facultad: {facultad_nombre}")
    
    def crear_fases_cronograma(self):
        fases_data = [
            (1, 'RC', 'Organización en Comisión de Rediseño Curricular'),
            (2, 'DI', 'Diagnóstico Inicial de la Carrera'),
            (3, 'EC', 'Estudio de Contexto'),
            (4, 'MM', 'Mesa Multisectorial'),
            (5, 'MC', 'Elaboración de la Propuesta Macro Curricular'),
            (6, 'RAC', 'Reunión Académica de Carrera'),
            (7, 'VT', 'Validación Técnica (Dpto. Gestión Curricular)'),
            (8, 'VN', 'Validación Normativa (Dirección Servicios Académicos)'),
            (9, 'CA', 'Comisión Académica'),
            (10, 'HCU', 'Honorable Consejo Universitario'),
            (11, 'RAN', 'Reunión Académica Nacional'),
        ]
        
        for orden, codigo, nombre in fases_data:
            FaseCronograma.objects.get_or_create(
                codigo=codigo,
                defaults={'nombre': nombre, 'orden': orden}
            )
    
    def crear_carreras_potosi(self):
        """Carreras de la sede principal Potosí"""
        potosi = Sede.objects.get(nombre='Potosí')
        
        carreras_potosi = [
            # Facultad de Artes
            ('Facultad de Artes', 'Artes Musicales', 'licenciatura'),
            ('Facultad de Artes', 'Artes Plásticas', 'licenciatura'),
            ('Facultad de Artes', 'Arquitectura', 'licenciatura'),
            
            # Facultad de Ciencias Agrícolas y Pecuarias
            ('Facultad de Ciencias Agrícolas y Pecuarias', 'Ingeniería Agronómica', 'licenciatura'),
            ('Facultad de Ciencias Agrícolas y Pecuarias', 'Ingeniería Agroindustrial', 'licenciatura'),
            ('Facultad de Ciencias Agrícolas y Pecuarias', 'Ingeniería en Desarrollo Rural', 'licenciatura'),
            
            # Facultad de Ciencias Económicas, Financieras y Administrativas
            ('Facultad de Ciencias Económicas, Financieras y Administrativas', 'Auditoría - Contaduría Pública', 'licenciatura'),
            ('Facultad de Ciencias Económicas, Financieras y Administrativas', 'Contabilidad y Finanzas', 'licenciatura'),
            ('Facultad de Ciencias Económicas, Financieras y Administrativas', 'Administración de Empresas', 'licenciatura'),
            ('Facultad de Ciencias Económicas, Financieras y Administrativas', 'Economía', 'licenciatura'),
            ('Facultad de Ciencias Económicas, Financieras y Administrativas', 'Ingeniería Comercial', 'licenciatura'),
            
            # Facultad de Ciencias Puras
            ('Facultad de Ciencias Puras', 'Química', 'licenciatura'),
            ('Facultad de Ciencias Puras', 'Estadística', 'licenciatura'),
            ('Facultad de Ciencias Puras', 'Física', 'licenciatura'),
            ('Facultad de Ciencias Puras', 'Matemática', 'licenciatura'),
            ('Facultad de Ciencias Puras', 'Ingeniería Informática', 'licenciatura'),
            
            # Facultad de Ciencias Sociales y Humanísticas
            ('Facultad de Ciencias Sociales y Humanísticas', 'Turismo', 'licenciatura'),
            ('Facultad de Ciencias Sociales y Humanísticas', 'Lingüística e Idiomas', 'licenciatura'),
            ('Facultad de Ciencias Sociales y Humanísticas', 'Trabajo Social', 'licenciatura'),
            ('Facultad de Ciencias Sociales y Humanísticas', 'Programa de Ciencias de la Comunicación', 'licenciatura'),
            ('Facultad de Ciencias Sociales y Humanísticas', 'Programa de Pedagogía Intercultural', 'licenciatura'),
            
            # Facultad de Derecho
            ('Facultad de Derecho', 'Derecho', 'licenciatura'),
            
            # Facultad de Ingeniería
            ('Facultad de Ingeniería', 'Ingeniería Civil', 'licenciatura'),
            ('Facultad de Ingeniería', 'Construcciones Civiles', 'tecnico_superior'),
            ('Facultad de Ingeniería', 'Ingeniería en Geodesia y Topografía', 'licenciatura'),
            
            # Facultad de Ingeniería Geológica
            ('Facultad de Ingeniería Geológica', 'Ingeniería Geológica', 'licenciatura'),
            ('Facultad de Ingeniería Geológica', 'Ingeniería del Medio Ambiente', 'licenciatura'),
            
            # Facultad de Ingeniería Minera
            ('Facultad de Ingeniería Minera', 'Ingeniería Minera', 'licenciatura'),
            ('Facultad de Ingeniería Minera', 'Ingeniería de Procesos de Materias Primas Minerales', 'licenciatura'),
            
            # Facultad de Ingeniería Tecnológica
            ('Facultad de Ingeniería Tecnológica', 'Ingeniería Eléctrica', 'licenciatura'),
            ('Facultad de Ingeniería Tecnológica', 'Ingeniería Electrónica', 'licenciatura'),
            ('Facultad de Ingeniería Tecnológica', 'Ingeniería Mecánica', 'licenciatura'),
            ('Facultad de Ingeniería Tecnológica', 'Ingeniería Mecatrónica', 'licenciatura'),
            ('Facultad de Ingeniería Tecnológica', 'Mecánica Automotriz', 'licenciatura'),
            ('Facultad de Ingeniería Tecnológica', 'Técnico Univ. Medio en Electricidad', 'tecnico_medio'),
            ('Facultad de Ingeniería Tecnológica', 'Técnico Univ. Medio en Electrónica', 'tecnico_medio'),
            ('Facultad de Ingeniería Tecnológica', 'Técnico Univ. Medio en Mecánica', 'tecnico_medio'),
            ('Facultad de Ingeniería Tecnológica', 'Técnico Univ. Medio en Mecatrónica', 'tecnico_medio'),
            ('Facultad de Ingeniería Tecnológica', 'Técnico Univ. Medio en Mecánica Automotriz', 'tecnico_medio'),
            
            # Facultad de Ciencias de la Salud
            ('Facultad de Ciencias de la Salud', 'Enfermería', 'licenciatura'),
            ('Facultad de Ciencias de la Salud', 'Técnico Univ. Medio Auxiliar de Enfermería', 'tecnico_medio'),
            
            # Facultad de Medicina
            ('Facultad de Medicina', 'Medicina', 'licenciatura'),
            
            # Vicerrectorado
            ('Vicerrectorado', 'Programa Enfermeria', 'licenciatura'),
            ('Vicerrectorado', 'Programa Derecho', 'licenciatura'),
            ('Vicerrectorado', 'Programa Ciencias de la Comunicación', 'licenciatura'),
            ('Vicerrectorado', 'Odontologia', 'licenciatura'),
            ('Vicerrectorado', 'Ingeniería de Sistemas', 'licenciatura'),
            ('Vicerrectorado', 'Programa Diseño y Programacion Digital', 'licenciatura'),
        ]
        
        for facultad_nombre, carrera_nombre, grado in carreras_potosi:
            facultad = Facultad.objects.get(nombre=facultad_nombre)
            carrera, created = Carrera.objects.get_or_create(
                facultad=facultad,
                nombre=carrera_nombre,
                sede=potosi,
                defaults={'grado_academico': grado}
            )
            if created:
                self.stdout.write(f"✅ Creada: {carrera_nombre} - {facultad_nombre} - Potosí")
    
    def crear_carreras_sedes_regionales(self):
        """Carreras de las sedes regionales"""
        
        # Tupiza
        tupiza = Sede.objects.get(nombre='Tupiza')
        carreras_tupiza = [
            ('Facultad de Ciencias Agrícolas y Pecuarias', 'Medicina Veterinaria y Zootecnia', 'licenciatura'),
            ('Facultad de Ciencias Económicas, Financieras y Administrativas', 'Contaduría Pública', 'licenciatura'),
            ('Vicerrectorado', 'Programa Derecho', 'licenciatura'),
            ('Vicerrectorado', 'Ingeniería de Sistemas', 'licenciatura'),
            ('Facultad de Ciencias Sociales y Humanísticas', 'Escuela de Idiomas', 'licenciatura'),
        ]
        
        # Villazón
        villazon = Sede.objects.get(nombre='Villazón')
        carreras_villazon = [
            ('Facultad de Ciencias Agrícolas y Pecuarias', 'Ingeniería Agropecuaria', 'licenciatura'),
            ('Facultad de Ciencias de la Salud', 'Enfermería', 'licenciatura'),
        ]
        
        # Uyuni
        uyuni = Sede.objects.get(nombre='Uyuni')
        carreras_uyuni = [
            ('Facultad de Ciencias Económicas, Financieras y Administrativas', 'Economía', 'licenciatura'),
            ('Facultad de Ciencias Sociales y Humanísticas', 'Turismo', 'licenciatura'),
            ('Facultad de Ciencias Sociales y Humanísticas', 'Lingüística e Idiomas', 'licenciatura'),
        ]
        
        # Uncía
        uncia = Sede.objects.get(nombre='Uncía')
        carreras_uncia = [
            ('Facultad de Ciencias Económicas, Financieras y Administrativas', 'Economía', 'licenciatura'),
            ('Facultad de Derecho', 'Derecho', 'licenciatura'),
            ('Facultad de Ciencias Sociales y Humanísticas', 'Trabajo Social', 'licenciatura'),
            ('Facultad de Ciencias Sociales y Humanísticas', 'Lingüística e Idiomas', 'licenciatura'),
        ]
        
        # Llica
        llica = Sede.objects.get(nombre='Llica')
        carreras_llica = [
            ('Vicerrectorado', 'Programa Enfermeria', 'licenciatura'),
        ]
        
        # San Cristóbal
        san_cristobal = Sede.objects.get(nombre='San Cristóbal')
        carreras_san_cristobal = [
            ('Facultad de Ciencias de la Salud', 'Técnico Univ. Medio Auxiliar de Enfermería', 'tecnico_medio'),
            ('Facultad de Ingeniería Tecnológica', 'Ingeniería Eléctrica', 'licenciatura'),
            ('Facultad de Ingeniería Tecnológica', 'Ingeniería Mecánica', 'licenciatura'),
            ('Facultad de Ingeniería Tecnológica', 'Ingeniería Mecatrónica', 'licenciatura'),
            ('Facultad de Ingeniería Tecnológica', 'Ingeniería Automotriz', 'licenciatura'),
        ]
        
        # Río Grande
        rio_grande = Sede.objects.get(nombre='Río Grande')
        carreras_rio_grande = [
            ('Facultad de Ciencias Económicas, Financieras y Administrativas', 'Administración de Empresas', 'licenciatura'),
        ]
        
        # Cargar todas las carreras regionales
        sedes_carreras = [
            (tupiza, carreras_tupiza),
            (villazon, carreras_villazon),
            (uyuni, carreras_uyuni),
            (uncia, carreras_uncia),
            (llica, carreras_llica),
            (san_cristobal, carreras_san_cristobal),
            (rio_grande, carreras_rio_grande),
        ]
        
        for sede, carreras in sedes_carreras:
            for facultad_nombre, carrera_nombre, grado in carreras:
                facultad = Facultad.objects.get(nombre=facultad_nombre)
                carrera, created = Carrera.objects.get_or_create(
                    facultad=facultad,
                    nombre=carrera_nombre,
                    sede=sede,
                    defaults={'grado_academico': grado}
                )
                if created:
                    self.stdout.write(f"✅ Creada: {carrera_nombre} - {facultad_nombre} - {sede.nombre}")