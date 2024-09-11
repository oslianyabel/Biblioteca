import pandas as pd
from django.core.management.base import BaseCommand
from app.models import Estudiante, Libro, Prestamo, ListaNegra  # Importa tus modelos

class Command(BaseCommand):
    help = 'Exporta datos de los modelos a un archivo Excel'

    def handle(self, *args, **kwargs):
        # Obtener datos de los modelos
        estudiantes = Estudiante.objects.all().values()
        libros = Libro.objects.all().values()
        prestamos = Prestamo.objects.all().values()
        lista_negra = ListaNegra.objects.all().values()

        # Convertir los datos a DataFrames de pandas
        df_estudiantes = pd.DataFrame(estudiantes)
        df_libros = pd.DataFrame(libros)
        df_prestamos = pd.DataFrame(prestamos)
        df_lista_negra = pd.DataFrame(lista_negra)

        # Crear un archivo Excel con múltiples hojas (sheet)
        with pd.ExcelWriter('app_data.xlsx', engine='openpyxl') as writer:
            df_estudiantes.to_excel(writer, sheet_name='Estudiantes', index=False)
            df_libros.to_excel(writer, sheet_name='Libros', index=False)
            df_prestamos.to_excel(writer, sheet_name='Prestamos', index=False)
            df_lista_negra.to_excel(writer, sheet_name='Lista Negra', index=False)

        self.stdout.write(self.style.SUCCESS('Datos exportados exitosamente a app_data.xlsx'))
