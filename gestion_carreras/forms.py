
from django import forms
from .models import EstadoCronograma, ArchivoCronograma

class EstadoCronogramaForm(forms.ModelForm):
    class Meta:
        model = EstadoCronograma
        fields = ['estado', 'fecha_inicio', 'fecha_conclusion', 'medios_verificacion', 'observaciones']
        widgets = {
            'estado': forms.Select(attrs={
                'class': 'form-select',
                'style': 'width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px;'
            }),
            'fecha_inicio': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'style': 'width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px;'
            }),
            'fecha_conclusion': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'style': 'width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px;'
            }),
            'medios_verificacion': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'style': 'width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px;',
                'placeholder': 'Describa los medios de verificación cumplidos...'
            }),
            'observaciones': forms.Textarea(attrs={
                'rows': 2,
                'class': 'form-control',
                'style': 'width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px;',
                'placeholder': 'Observaciones adicionales...'
            }),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_conclusion = cleaned_data.get('fecha_conclusion')
        
        if fecha_inicio and fecha_conclusion and fecha_conclusion < fecha_inicio:
            raise forms.ValidationError("La fecha de conclusión no puede ser anterior a la fecha de inicio.")
        
        return cleaned_data

class ArchivoCronogramaForm(forms.ModelForm):
    class Meta:
        model = ArchivoCronograma
        fields = ['archivo', 'tipo', 'nombre', 'descripcion']
        widgets = {
            'archivo': forms.FileInput(attrs={
                'class': 'form-control',
                'style': 'width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px;'
            }),
            'tipo': forms.Select(attrs={
                'class': 'form-select',
                'style': 'width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px;'
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px;',
                'placeholder': 'Ej: Acta de Comisión Académica - Revisión Curricular'
            }),
            'descripcion': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'style': 'width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px;',
                'placeholder': 'Describa el contenido del archivo...'
            }),
        }
    
    def clean_archivo(self):
        archivo = self.cleaned_data.get('archivo')
        if archivo:
            # Validar tamaño (10MB máximo)
            if archivo.size > 10 * 1024 * 1024:
                raise forms.ValidationError("El archivo no puede ser mayor a 10MB")
            
            # Validar extensiones
            extensiones_permitidas = ['.pdf', '.doc', '.docx', '.jpg', '.jpeg', '.png']
            import os
            ext = os.path.splitext(archivo.name)[1].lower()
            if ext not in extensiones_permitidas:
                raise forms.ValidationError(f"Tipo de archivo no permitido. Use: {', '.join(extensiones_permitidas)}")
        
        return archivo