from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import *

urlpatterns = [
    # URLs para Estudiante
    path('estudiantes/', EstudianteListView.as_view(), name='estudiante-list'),
    path('estudiantes/<int:pk>/', EstudianteDetailView.as_view(), name='estudiante-detail'),
    path('estudiantes/nuevo/', EstudianteCreateView.as_view(), name='estudiante-create'),
    path('estudiantes/<int:pk>/editar/', EstudianteUpdateView.as_view(), name='estudiante-update'),
    path('estudiantes/<int:pk>/eliminar/', EstudianteDeleteView.as_view(), name='estudiante-delete'),
    
    # URLs para Lista Negra
    path('lista_negra/', ListaNegraListView.as_view(), name='lista_negra-list'),
    path('lista_negra/sacar_estudiante/<int:pk>/', sacar_estudiante, name='sacar_estudiante'),

    # URLs para Libro
    path('libros/', LibroListView.as_view(), name='libro-list'),
    path('libros/<int:pk>/', LibroDetailView.as_view(), name='libro-detail'),
    path('libros/nuevo/', LibroCreateView.as_view(), name='libro-create'),
    path('libros/<int:pk>/editar/', LibroUpdateView.as_view(), name='libro-update'),
    path('libros/<int:pk>/eliminar/', LibroDeleteView.as_view(), name='libro-delete'),

    # URLs para Prestamo
    path('prestamos/', PrestamoListView.as_view(), name='prestamo-list'),
    path('prestamos/<int:pk>/', PrestamoDetailView.as_view(), name='prestamo-detail'),
    path('prestamos/nuevo/', PrestamoCreateView.as_view(), name='prestamo-create'),
    path('prestamos/<int:pk>/editar/', PrestamoUpdateView.as_view(), name='prestamo-update'),
    path('prestamos/<int:pk>/eliminar/', PrestamoDeleteView.as_view(), name='prestamo-delete'),
    
    #Extra
    path('login/', user_login, name='login'),
    path('accounts/login/', user_login, name='login'),
    path('logout/', LogoutView.as_view(next_page="/login"), name='logout'),
    path('confirmar_promo/', confirmar_promo, name='confirmar_promo'),
    path('devolver_libro/<int:libro_id>/<int:estudiante_id>', devolver_libro, name='devolver_libro'),
]
