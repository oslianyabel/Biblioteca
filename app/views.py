from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from .models import Estudiante, Libro, Prestamo

# Listar estudiantes
class EstudianteListView(ListView):
    model = Estudiante
    template_name = 'estudiante_list.html'
    context_object_name = 'estudiantes'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['role'] = None
        grupos = list(user.groups.values_list('name', flat=True))
        if "administrador" in grupos:
            context['role'] = "administrador"
        elif "directivo" in grupos:
            context['role'] = "directivo"
        elif "bibliotecario" in grupos:
            context['role'] = "bibliotecario"
            
        return context

# Detalles de un estudiante
class EstudianteDetailView(DetailView):
    model = Estudiante
    template_name = 'estudiante_detail.html'

# Crear un nuevo estudiante
class EstudianteCreateView(CreateView):
    model = Estudiante
    template_name = 'form.html'
    fields = ['nombre', 'apellidos', 'edad', 'anno_academico', 'CI', 'telefono']
    success_url = reverse_lazy('estudiante-list')

# Actualizar un estudiante
class EstudianteUpdateView(UpdateView):
    model = Estudiante
    template_name = 'form.html'
    fields = ['nombre', 'apellidos', 'edad', 'anno_academico', 'CI', 'telefono']
    success_url = reverse_lazy('estudiante-list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['role'] = None
        grupos = list(user.groups.values_list('name', flat=True))
        if "administrador" in grupos:
            context['role'] = "administrador"
        elif "directivo" in grupos:
            context['role'] = "directivo"
        elif "bibliotecario" in grupos:
            context['role'] = "bibliotecario"
            
        return context

# Eliminar un estudiante
class EstudianteDeleteView(DeleteView):
    model = Estudiante
    template_name = 'estudiante_confirm_delete.html'
    success_url = reverse_lazy('estudiante-list')


#=================================================LIBROS==============================================================
# Listar libros
class LibroListView(ListView):
    model = Libro
    template_name = 'libro_list.html'
    context_object_name = 'libros'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['role'] = None
        grupos = list(user.groups.values_list('name', flat=True))
        if "administrador" in grupos:
            context['role'] = "administrador"
        elif "directivo" in grupos:
            context['role'] = "directivo"
        elif "bibliotecario" in grupos:
            context['role'] = "bibliotecario"
            
        return context

# Detalles de un libro
class LibroDetailView(DetailView):
    model = Libro
    template_name = 'libro_detail.html'

# Crear un nuevo libro
class LibroCreateView(CreateView):
    model = Libro
    template_name = 'form.html'
    fields = ['titulo', 'categoria', 'cantidad_disponible', 'cantidad_prestada', 'autor', 'editorial', 'descripcion']
    success_url = reverse_lazy('libro-list')

# Actualizar un libro
class LibroUpdateView(UpdateView):
    model = Libro
    template_name = 'form.html'
    fields = ['titulo', 'categoria', 'cantidad_disponible', 'cantidad_prestada', 'autor', 'editorial', 'descripcion']
    success_url = reverse_lazy('libro-list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['role'] = None
        grupos = list(user.groups.values_list('name', flat=True))
        if "administrador" in grupos:
            context['role'] = "administrador"
        elif "directivo" in grupos:
            context['role'] = "directivo"
        elif "bibliotecario" in grupos:
            context['role'] = "bibliotecario"
            
        return context

# Eliminar un libro
class LibroDeleteView(DeleteView):
    model = Libro
    template_name = 'libro_confirm_delete.html'
    success_url = reverse_lazy('libro-list')


#==================================================Préstamos====================================================
# Listar préstamos
class PrestamoListView(ListView):
    model = Prestamo
    template_name = 'prestamo_list.html'
    context_object_name = 'prestamos'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['role'] = None
        grupos = list(user.groups.values_list('name', flat=True))
        if "administrador" in grupos:
            context['role'] = "administrador"
        elif "directivo" in grupos:
            context['role'] = "directivo"
        elif "bibliotecario" in grupos:
            context['role'] = "bibliotecario"
            
        return context

# Detalles de un préstamo
class PrestamoDetailView(DetailView):
    model = Prestamo
    template_name = 'prestamo_detail.html'

# Crear un nuevo préstamo
class PrestamoCreateView(CreateView):
    model = Prestamo
    template_name = 'form.html'
    fields = ['fecha', 'estudiante', 'libro']
    success_url = reverse_lazy('prestamo-list')

# Actualizar un préstamo
class PrestamoUpdateView(UpdateView):
    model = Prestamo
    template_name = 'form.html'
    fields = ['fecha', 'estudiante', 'libro']
    success_url = reverse_lazy('prestamo-list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['role'] = None
        grupos = list(user.groups.values_list('name', flat=True))
        if "administrador" in grupos:
            context['role'] = "administrador"
        elif "directivo" in grupos:
            context['role'] = "directivo"
        elif "bibliotecario" in grupos:
            context['role'] = "bibliotecario"
            
        return context

# Eliminar un préstamo
class PrestamoDeleteView(DeleteView):
    model = Prestamo
    template_name = 'prestamo_confirm_delete.html'
    success_url = reverse_lazy('prestamo-list')


#=====================================================LOGIN=====================================================
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('libro-list')
    else:
        form = AuthenticationForm()
    return render(request, 'app/login.html', {'form': form})
