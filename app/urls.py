from django.urls import path
from .views import *

urlpatterns = [
    # URLs para Estudiante
    path('estudiantes/', EstudianteListView.as_view(), name='estudiante-list'),
    path('estudiantes/<int:pk>/', EstudianteDetailView.as_view(), name='estudiante-detail'),
    path('estudiantes/nuevo/', EstudianteCreateView.as_view(), name='estudiante-create'),
    path('estudiantes/<int:pk>/editar/', EstudianteUpdateView.as_view(), name='estudiante-update'),
    path('estudiantes/<int:pk>/eliminar/', EstudianteDeleteView.as_view(), name='estudiante-delete'),

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
]
