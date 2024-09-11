from django.test import TestCase
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group
from django.test import Client
from unittest.mock import patch
from .models import *
from .views import *

#==============================================Modelos=======================================================
#==============================================Libro=======================================================
class LibroTestCase(TestCase):
    def setUp(self):
        self.libro = Libro.objects.create(
            titulo="Libro de Prueba",
            categoria="programacion",
            cantidad_disponible=5,
            cantidad_prestada=0,
            autor="Autor de Prueba",
            editorial="Editorial de Prueba",
            descripcion="Descripción de prueba"
        )
    
    def test_prestar_libro(self):
        self.assertTrue(self.libro.prestar())
        self.assertEqual(self.libro.cantidad_disponible, 4)
        self.assertEqual(self.libro.cantidad_prestada, 1)

    def test_prestar_libro_no_disponible(self):
        self.libro.cantidad_disponible = 0
        self.libro.save()
        self.assertFalse(self.libro.prestar())

    def test_devolver_libro(self):
        self.libro.prestar()
        self.assertTrue(self.libro.devolver())
        self.assertEqual(self.libro.cantidad_disponible, 5)
        self.assertEqual(self.libro.cantidad_prestada, 0)

    def test_devolver_libro_no_prestado(self):
        self.assertFalse(self.libro.devolver())


#==============================================Estudiante=======================================================
class EstudianteTestCase(TestCase):
    def setUp(self):
        self.estudiante = Estudiante.objects.create(
            nombre="Juan",
            apellidos="Pérez",
            edad=20,
            anno_academico=2,
            CI="12345678901",
            telefono="12345678"
        )
        self.libro = Libro.objects.create(
            titulo="Libro de Prueba",
            categoria="programacion",
            cantidad_disponible=5,
            cantidad_prestada=0,
            autor="Autor de Prueba",
            editorial="Editorial de Prueba",
            descripcion="Descripción de prueba"
        )

    def test_promover(self):
        Estudiante.promover()
        self.estudiante.refresh_from_db()
        self.assertEqual(self.estudiante.anno_academico, 3)

    def test_eliminar_graduados(self):
        self.estudiante.anno_academico = 6
        self.estudiante.save()
        Estudiante.eliminar_graduados()
        self.assertFalse(Estudiante.objects.filter(id=self.estudiante.id).exists())

    def test_cantidad_prestamos(self):
        Prestamo.objects.create(fecha="2023-09-09", estudiante=self.estudiante, libro=self.libro)
        self.assertEqual(self.estudiante.cantidad_prestamos, 1)


#==============================================Préstamo y Lista Negra============================================
class PrestamoListaNegraTestCase(TestCase):
    def setUp(self):
        self.estudiante = Estudiante.objects.create(
            nombre="Juan",
            apellidos="Pérez",
            edad=20,
            anno_academico=2,
            CI="12345678901",
            telefono="12345678"
        )
        self.libro = Libro.objects.create(
            titulo="Libro de Prueba",
            categoria="programacion",
            cantidad_disponible=5,
            cantidad_prestada=0,
            autor="Autor de Prueba",
            editorial="Editorial de Prueba",
            descripcion="Descripción de prueba"
        )
        self.prestamo = Prestamo.objects.create(fecha="2023-09-09", estudiante=self.estudiante, libro=self.libro)
        self.lista_negra = ListaNegra.objects.create(fecha="2023-09-10", estudiante=self.estudiante, libro=self.libro)

    def test_str_prestamo(self):
        self.assertEqual(str(self.prestamo), "2023-09-09")

    def test_str_lista_negra(self):
        self.assertEqual(str(self.lista_negra), "2023-09-10")


#==============================================Vistas=======================================================
#==============================================Estudiante=======================================================
class EstudianteViewTests(TestCase):
    def setUp(self):
        # Crear un usuario y un grupo
        self.directivo_group = Group.objects.create(name='directivo')
        self.user = User.objects.create_user(username='admin', password='password')
        self.user.groups.add(self.directivo_group)
        
        self.estudiante = Estudiante.objects.create(
            nombre="Juan",
            apellidos="Pérez",
            edad=20,
            anno_academico=2,
            CI="12345678901",
            telefono="12345678"
        )
        self.client = Client()

    def test_estudiante_list_view(self):
        response = self.client.get(reverse('estudiante-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Juan")
        self.assertTemplateUsed(response, 'app/estudiante_list.html')

    def test_estudiante_detail_view(self):
        response = self.client.get(reverse('estudiante-detail', args=[self.estudiante.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Juan")
        self.assertTemplateUsed(response, 'app/estudiante_detail.html')

    def test_estudiante_create_view(self):
        # Simular que el usuario está autenticado y tiene permisos
        self.client.login(username='admin', password='password')
        response = self.client.post(reverse('estudiante-create'), {
            'nombre': 'Ana',
            'apellidos': 'García',
            'edad': 21,
            'anno_academico': 3,
            'CI': '12345678902',
            'telefono': '87654321'
        })
        self.assertEqual(response.status_code, 302)  # Redirige después de la creación
        self.assertTrue(Estudiante.objects.filter(nombre="Ana").exists())

    def test_estudiante_update_view(self):
        self.client.login(username='admin', password='password')
        response = self.client.post(reverse('estudiante-update', args=[self.estudiante.id]), {
            'nombre': 'Juan',
            'apellidos': 'Pérez',
            'edad': 21,  # Cambiar la edad
            'anno_academico': 2,
            'CI': '12345678901',
            'telefono': '12345678'
        })
        self.assertEqual(response.status_code, 302)
        self.estudiante.refresh_from_db()
        self.assertEqual(self.estudiante.edad, 21)

    def test_estudiante_delete_view(self):
        self.client.login(username='admin', password='password')
        response = self.client.post(reverse('estudiante-delete', args=[self.estudiante.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Estudiante.objects.filter(id=self.estudiante.id).exists())


#==============================================Libro=======================================================
class LibroViewTests(TestCase):
    def setUp(self):
        self.bibliotecario_group = Group.objects.create(name='bibliotecario')
        self.user = User.objects.create_user(username='admin', password='password')
        self.user.groups.add(self.bibliotecario_group)

        self.libro = Libro.objects.create(
            titulo="Libro de Prueba",
            categoria="programacion",
            cantidad_disponible=5,
            cantidad_prestada=0,
            autor="Autor de Prueba",
            editorial="Editorial de Prueba",
            descripcion="Descripción de prueba"
        )
        self.client = Client()

    def test_libro_list_view(self):
        response = self.client.get(reverse('libro-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Libro de Prueba")
        self.assertTemplateUsed(response, 'app/libro_list.html')

    def test_libro_detail_view(self):
        response = self.client.get(reverse('libro-detail', args=[self.libro.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Libro de Prueba")
        self.assertTemplateUsed(response, 'app/libro_detail.html')

    def test_libro_create_view(self):
        self.client.login(username='admin', password='password')
        response = self.client.post(reverse('libro-create'), {
            'titulo': 'Nuevo Libro',
            'categoria': 'programacion',
            'cantidad_disponible': 5,
            'cantidad_prestada': 0,
            'autor': 'Nuevo Autor',
            'editorial': 'Nueva Editorial',
            'descripcion': 'Descripción del nuevo libro'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Libro.objects.filter(titulo="Nuevo Libro").exists())

    def test_libro_update_view(self):
        self.client.login(username='admin', password='password')
        response = self.client.post(reverse('libro-update', args=[self.libro.id]), {
            'titulo': 'Libro Actualizado',
            'categoria': 'programacion',
            'cantidad_disponible': 5,
            'cantidad_prestada': 0,
            'autor': 'Autor Actualizado',
            'editorial': 'Editorial Actualizada',
            'descripcion': 'Descripción actualizada'
        })
        self.assertEqual(response.status_code, 302)
        self.libro.refresh_from_db()
        self.assertEqual(self.libro.titulo, 'Libro Actualizado')

    def test_libro_delete_view(self):
        self.client.login(username='admin', password='password')
        response = self.client.post(reverse('libro-delete', args=[self.libro.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Libro.objects.filter(id=self.libro.id).exists())


#==============================================Extra=======================================================
#==============================================Promover Año=======================================================
class PromoverAnnoTests(TestCase):
    def setUp(self):
        self.libro = Libro.objects.create(
            titulo="Libro de Prueba",
            categoria="programacion",
            cantidad_disponible=5,
            cantidad_prestada=0,
            autor="Autor de Prueba",
            editorial="Editorial de Prueba",
            descripcion="Descripción de prueba"
        )
        
        self.estudiante = Estudiante.objects.create(
            nombre="Juan",
            apellidos="Pérez",
            edad=20,
            anno_academico=2,
            CI="12345678901",
            telefono="12345678"
        )
        
        self.prestamo = Prestamo.objects.create(
            fecha="2024-09-01",
            estudiante=self.estudiante,
            libro=self.libro
        )

    def test_promover_anno(self):
        result = promover_anno()
        self.assertTrue(result)
        self.assertTrue(ListaNegra.objects.filter(
            estudiante=self.estudiante, libro=self.libro).exists())
        self.assertFalse(Prestamo.objects.filter(
            estudiante=self.estudiante, libro=self.libro).exists())
        self.assertEqual(Estudiante.objects.get(id=self.estudiante.id).anno_academico, 3)
        self.assertFalse(Estudiante.objects.filter(anno_academico__gt=5).exists())

