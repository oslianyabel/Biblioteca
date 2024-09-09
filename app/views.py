from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from .models import Estudiante, Libro, Prestamo
from.forms import *
from django.urls import reverse

def group_required(rol):
    """
    Función auxiliar para verificar si el usuario pertenece a un grupo específico.
    """
    def in_group(user):
        roles = list(user.groups.values_list('name', flat=True))
        if "administrador" in roles:
            return True
        
        print(roles)
        return rol in roles
    
    return user_passes_test(in_group)

# Listar estudiantes
class EstudianteListView(ListView):
    model = Estudiante
    template_name = 'estudiante_list.html'
    context_object_name = 'estudiantes'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        estudiantes = Estudiante.objects.all()
        paginator = Paginator(estudiantes, 10)
        page = self.request.GET.get("page")
        estudiantes = paginator.get_page(page)
        context["estudiantes"] = estudiantes
        
        return context

# Detalles de un estudiante
class EstudianteDetailView(DetailView):
    model = Estudiante
    template_name = 'app/estudiante_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        estudiante = self.get_object()
        libros_prestados = Libro.objects.filter(prestamo__estudiante=estudiante)
        context['libros'] = libros_prestados
        
        return context

# Crear un nuevo estudiante
@method_decorator(group_required('directivo'), name='dispatch')
class EstudianteCreateView(CreateView):
    model = Estudiante
    template_name = 'app/form.html'
    form_class = EstudianteForm
    success_url = reverse_lazy('estudiante-list')

# Actualizar un estudiante
@method_decorator(group_required('directivo'), name='dispatch')
class EstudianteUpdateView(UpdateView):
    model = Estudiante
    template_name = 'app/form.html'
    form_class = EstudianteForm
    success_url = reverse_lazy('estudiante-list')
    
# Eliminar un estudiante
@method_decorator(group_required('directivo'), name='dispatch')
class EstudianteDeleteView(DeleteView):
    model = Estudiante
    template_name = 'app/estudiante_confirm_delete.html'
    success_url = reverse_lazy('estudiante-list')


#=================================================LIBROS==============================================================
# Listar libros
class LibroListView(ListView):
    model = Libro
    template_name = 'libro_list.html'
    context_object_name = 'libros'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        libros = Libro.objects.all()
        paginator = Paginator(libros, 10)
        page = self.request.GET.get("page")
        libros = paginator.get_page(page)
        context["libros"] = libros
            
        return context

# Detalles de un libro
class LibroDetailView(DetailView):
    model = Libro
    template_name = 'libro_detail.html'

# Crear un nuevo libro
@method_decorator(group_required('bibliotecario'), name='dispatch')
class LibroCreateView(CreateView):
    model = Libro
    template_name = 'app/form.html'
    form_class = LibroForm
    success_url = reverse_lazy('libro-list')

# Actualizar un libro
@method_decorator(group_required('bibliotecario'), name='dispatch')
class LibroUpdateView(UpdateView):
    model = Libro
    template_name = 'app/form.html'
    form_class = LibroForm
    success_url = reverse_lazy('libro-list')
    
# Eliminar un libro
@method_decorator(group_required('bibliotecario'), name='dispatch')
class LibroDeleteView(DeleteView):
    model = Libro
    template_name = 'app/libro_confirm_delete.html'
    success_url = reverse_lazy('libro-list')


#==================================================Préstamos====================================================
# Listar préstamos
class PrestamoListView(ListView):
    model = Prestamo
    template_name = 'prestamo_list.html'
    context_object_name = 'prestamos'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        prestamos = Prestamo.objects.all()
        paginator = Paginator(prestamos, 10)
        page = self.request.GET.get("page")
        prestamos = paginator.get_page(page)
        context["prestamos"] = prestamos
            
        return context

# Detalles de un préstamo
class PrestamoDetailView(DetailView):
    model = Prestamo
    template_name = 'prestamo_detail.html'

# Crear un nuevo préstamo
@method_decorator(group_required('bibliotecario'), name='dispatch')
class PrestamoCreateView(CreateView):
    model = Prestamo
    template_name = 'app/form.html'
    form_class = PrestamoForm
    success_url = reverse_lazy('prestamo-list')
    
    def form_valid(self, form):
        prestamo = form.save()
        prestamo.libro.prestar()

        return super().form_valid(form)

# Actualizar un préstamo
@method_decorator(group_required('bibliotecario'), name='dispatch')
class PrestamoUpdateView(UpdateView):
    model = Prestamo
    template_name = 'app/form.html'
    form_class = PrestamoForm
    success_url = reverse_lazy('prestamo-list')
    
# Eliminar un préstamo
@method_decorator(group_required('bibliotecario'), name='dispatch')
class PrestamoDeleteView(DeleteView):
    model = Prestamo
    template_name = 'app/prestamo_confirm_delete.html'
    success_url = reverse_lazy('prestamo-list')
    
    def delete(self, request, *args, **kwargs):
        prestamo = self.get_object()
        prestamo.libro.devolver()
        
        return super().delete(request, *args, **kwargs)


#=====================================================LISTA NEGRA===============================================
# Listar estudiantes en lista negra
@method_decorator(group_required('directivo'), name='dispatch')
class ListaNegraListView(ListView):
    model = Estudiante
    template_name = 'app/lista_negra.html'
    context_object_name = 'estudiantes'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        estudiantes = Estudiante.lista_negra()
        paginator = Paginator(estudiantes, 10)
        page = self.request.GET.get("page")
        estudiantes = paginator.get_page(page)
        context["estudiantes"] = estudiantes
        
        return context

# Eliminar un estudiante de la lista negra con todas las devoluciones realizadas
@group_required('directivo')
def sacar_estudiante(request, pk):
    if request.method == "GET":
        estudiante = Estudiante.objects.get(pk = pk)
        
        prestamos_estudiante = ListaNegra.objects.filter(estudiante=estudiante)
        
        for prestamo in prestamos_estudiante:
            prestamo.libro.devolver()
        
        prestamos_estudiante.delete()
        return redirect("lista_negra-list")
    
    

#=====================================================EXTRA=====================================================
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('libro-list')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


def promover_anno():
    prestamos = Prestamo.objects.all()
    
    for prestamo in prestamos:
        ListaNegra.objects.create(
            fecha=prestamo.fecha,
            estudiante=prestamo.estudiante,
            libro=prestamo.libro
        )
    
    prestamos.delete()
    Estudiante.promover()
    Estudiante.eliminar_graduados()
    
    return True


def confirmar_promo(request):
    if request.method == 'POST':
        # Confirmación del usuario
        promover_anno()
        return redirect('estudiante-list')
    
    return render(request, 'app/confirmar_promo.html')


def devolver_libro(request, libro_id, estudiante_id):
    libro = Libro.objects.get(id = libro_id)
    estudiante = Estudiante.objects.get(id = estudiante_id)
    prestamos = Prestamo.objects.all()
    
    libro.devolver()
    prestamos.filter(estudiante=estudiante, libro=libro).delete()
    
    return redirect(reverse("estudiante-detail", kwargs={"pk":estudiante_id}))
    