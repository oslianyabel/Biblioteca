from django.db import models
from django.core.validators import RegexValidator
from django.db.models import Q

LIBRO_CATEGORIA = [
    ("programacion", "Programación"),
    ("matematica", "Matemática"),
    ("sistemas operativos", "Sistemas operativos"),
    ("ingenieria de software", "Ingeniería de software"),
    ("compilacion", "Compilación"),
    ("redes de computadoras", "Redes de computadoras"),
    ("estadistica", "Estadística"),
    ("letras", "Letras"),
    ("investigacion de operaciones", "Investigación de operaciones"),
    ("inteligencia artificial", "Inteligencia artificial"),
    ("bases de datos", "Bases de datos"),
]

class Libro(models.Model):
    titulo = models.CharField(max_length=30)
    categoria = models.CharField(max_length=30, choices=LIBRO_CATEGORIA)
    cantidad_disponible = models.IntegerField()
    cantidad_prestada = models.IntegerField()
    autor = models.CharField(max_length=30)
    editorial = models.CharField(max_length=30)
    descripcion = models.TextField()
    
    def __str__(self) -> str:
        return self.titulo
    
    def prestar(self):
        if self.cantidad_disponible > 0:
            self.cantidad_prestada += 1
            self.cantidad_disponible -= 1
            self.save()
            return True
        else:
            return False
        
    def devolver(self):
        if self.cantidad_prestada > 0:
            self.cantidad_prestada -= 1
            self.cantidad_disponible += 1
            self.save()
            return True
        else:
            return False 


class Estudiante(models.Model):
    nombre = models.CharField(max_length=30)
    apellidos = models.CharField(max_length=30)
    edad = models.IntegerField()
    anno_academico = models.IntegerField()
    CI = models.CharField(max_length=11, unique=True, validators=[RegexValidator(r'^\d{11}$')])
    telefono = models.CharField(max_length=8, validators=[RegexValidator(r'^\d{8}$')])
    
    def __str__(self) -> str:
        return self.nombre
    
    @property
    def cantidad_prestamos(self):
        return self.prestamo_set.count() + self.listanegra_set.count()
    
    @classmethod
    def prestamos(cls):
        return cls.objects.filter(prestamo__isnull=False).distinct()
    
    @classmethod
    def lista_negra(cls):
        return cls.objects.filter(listanegra__isnull=False).distinct()
    
    @classmethod
    def promover(cls):
        cls.objects.update(anno_academico=models.F('anno_academico') + 1)
        
    @classmethod
    def eliminar_graduados(cls):
        cls.objects.filter(
            Q(prestamo__isnull=True) &
            Q(anno_academico__gt=5)
        ).delete()


class Prestamo(models.Model):
    fecha = models.DateField()
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.fecha


class ListaNegra(models.Model):
    fecha = models.DateField()
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.fecha
