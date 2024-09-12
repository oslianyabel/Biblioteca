from faker import Faker
from random import choice, randint
from datetime import timedelta, date
from app.models import Libro, Estudiante, Prestamo, ListaNegra

# Inicializar Faker
faker = Faker()

# Lista de categorías de libros
LIBRO_CATEGORIAS = [
    "programacion", "matematica", "sistemas operativos", 
    "ingenieria de software", "compilacion", "redes de computadoras", 
    "estadistica", "letras", "investigacion de operaciones", 
    "inteligencia artificial", "bases de datos"
]

# Borrar todas las instancias
Estudiante.objects.all().delete()
Libro.objects.all().delete()
Prestamo.objects.all().delete()
ListaNegra.objects.all().delete()

# Crear libros de prueba
for _ in range(50):
    libro = Libro(
        titulo=faker.sentence(nb_words=3),
        categoria=choice(LIBRO_CATEGORIAS),
        cantidad_disponible=randint(10, 1000),
        cantidad_prestada=0,  # Inicialmente sin préstamos
        autor=faker.name(),
        editorial=faker.company(),
        descripcion=faker.text(max_nb_chars=200)
    )
    libro.save()
    print(f"Libro '{libro.titulo}' creado")

# Crear estudiantes de prueba
for _ in range(30):
    estudiante = Estudiante(
        nombre=faker.first_name(),
        apellidos=faker.last_name(),
        edad=randint(18, 25),
        anno_academico=randint(1, 5),
        CI=faker.unique.random_number(digits=11),
        telefono=faker.unique.random_number(digits=8)
    )
    estudiante.save()
    print(f"Estudiante '{estudiante.nombre} {estudiante.apellidos}' creado")

# Crear préstamos de prueba
for _ in range(200):
    libro = choice(Libro.objects.filter(cantidad_disponible__gt=0))
    estudiante = choice(Estudiante.objects.all())
    prestamo = Prestamo(
        fecha=faker.date_between(start_date="-30d", end_date="today"),
        estudiante=estudiante,
        libro=libro
    )
    prestamo.save()
    libro.prestar()  # Prestar el libro
    print(f"Préstamo creado: Libro '{libro.titulo}' prestado a {estudiante.nombre}")
