from django.core.exceptions import ValidationError
from django import forms
from .models import *

class EstudianteForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = ["nombre", "apellidos", "edad", "anno_academico", "CI", "telefono"]
        labels = {
            "nombre": "Nombre",
            "apellidos": "Apellidos",
            "edad": "Edad",
            "anno_academico": "Año Académico",
            "CI": "CI",
            "telefono": "Teléfono",
        },
        widgets = {
            "nombre": forms.TextInput(
                attrs = {
                    "class": "form-control",
                    "placeholder": "Ej: Juan"
                }
            ),
            "apellidos": forms.TextInput(
                attrs = {
                    "class": "form-control",
                    "placeholder": "Ej: Pérez Pérez"
                }
            ),
            "edad": forms.NumberInput(
                attrs = {
                    "class": "form-control",
                    "placeholder": "Ej: 20"
                }
            ),
            "anno_academico": forms.NumberInput(
                attrs = {
                    "class": "form-control",
                    "placeholder": "Ej: 1"
                }
            ),
            "CI": forms.TextInput(
                attrs = {
                    "class": "form-control",
                    "placeholder": "Carnet de Identidad"
                }
            ),
            "telefono": forms.TextInput(
                attrs = {
                    "class": "form-control",
                    "placeholder": "## ## ## ##"
                }
            ),
        }
        
    def clean_CI(self):
        ci = self.cleaned_data.get('CI')
        if not ci.isdigit():
            raise ValidationError('El CI debe contener solo números.')
        if len(ci) != 11:
            raise ValidationError('El CI debe tener exactamente 11 dígitos.')
        
        return ci

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if not telefono.isdigit():
            raise ValidationError('El teléfono debe contener solo números')
        if len(telefono) != 8:
            raise ValidationError('El teléfono debe tener exactamente 8 dígitos')
        
        return telefono
    
    def clean_edad(self):
        edad = self.cleaned_data.get('edad')
        if edad < 0:
            raise ValidationError('Valores negativos no son aceptados')
        if edad < 16:
            raise ValidationError('Demasiado jóven')
        
        return edad
    

class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = ["titulo", "categoria", "cantidad_disponible", "cantidad_prestada", "autor", "editorial", "descripcion"]
        labels = {
            "titulo": "Título",
            "categoria": "Categoría",
            "cantidad_disponible": "Cantidad Disponible",
            "cantidad_prestada": "Cantidad Prestada",
            "autor": "Autor",
            "editorial": "Editorial",
            "descripcion": "Descripción",
        },
        widgets = {
            "titulo": forms.TextInput(
                attrs = {
                    "class": "form-control",
                    "placeholder": "Ej: Cálculo I"
                }
            ),
            "categoria": forms.Select(
                attrs = {"class": "form-control"},
                choices = LIBRO_CATEGORIA
            ),
            "cantidad_disponible": forms.NumberInput(
                attrs = {
                    "class": "form-control",
                    "placeholder": "###"
                }
            ),
            "cantidad_prestada": forms.NumberInput(
                attrs = {
                    "class": "form-control",
                    "placeholder": "###"
                }
            ),
            "autor": forms.TextInput(
                attrs = {
                    "class": "form-control",
                    "placeholder": "Nombre del Autor"
                }
            ),
            "editorial": forms.TextInput(
                attrs = {
                    "class": "form-control",
                    "placeholder": "Ej: MES"
                }
            ),
            "descripcion": forms.Textarea(
                attrs = {
                    "class": "form-control",
                    "placeholder": "Descripción del libro"
                }
            )
        }
        
    def clean_cantidad_disponible(self):
        cantidad_disponible = self.cleaned_data.get('cantidad_disponible')
        if cantidad_disponible < 0:
            raise ValidationError('Valores negativos no son aceptados')
        
        return cantidad_disponible

    def clean_cantidad_prestada(self):
        cantidad_prestada = self.cleaned_data.get('cantidad_prestada')
        if cantidad_prestada < 0:
            raise ValidationError('Valores negativos no son aceptados')
        
        return cantidad_prestada
    
class PrestamoForm(forms.ModelForm):
    class Meta:
        model = Prestamo
        fields = ["fecha", "estudiante", "libro"]
        labels = {
            "fecha": "Fecha",
            "estudiante": "Estudiante",
            "libro": "Libro"
        },
        widgets = {
            "fecha": forms.DateInput(
                attrs = {
                    "class": "form-control",
                    "type": "date"
                }
            ),
            "estudiante": forms.Select(
                attrs={"class": "form-control"}
            ),
            "libro": forms.Select(
                attrs={"class": "form-control"}
            )
        }
        
    def __init__(self, *args, **kwargs):
        super(PrestamoForm, self).__init__(*args, **kwargs)
        self.fields['estudiante'].queryset = Estudiante.objects.all()
        self.fields['libro'].queryset = Libro.objects.all()
        
    def clean_libro(self):
        libro = self.cleaned_data.get('libro')
        estudiante = self.cleaned_data.get('estudiante')
        if Prestamo.objects.filter(estudiante=estudiante, libro=libro).exists():
            raise ValidationError(f"{estudiante} ya tiene un ejemplar de {libro}")
        
        return libro
        