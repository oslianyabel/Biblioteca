from django.db import models
from django.core.validators import RegexValidator

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


class Estudiante(models.Model):
    nombre = models.CharField(max_length=30)
    apellidos = models.CharField(max_length=30)
    edad = models.IntegerField()
    anno_academico = models.IntegerField()
    CI = models.CharField(max_length=11, unique=True, validators=[RegexValidator(r'^\d{11}$')])
    telefono = models.CharField(max_length=8, validators=[RegexValidator(r'^\d{8}$')])
    
    def __str__(self) -> str:
        return self.nombre
    

class Prestamo(models.Model):
    fecha = models.DateField()
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.fecha
