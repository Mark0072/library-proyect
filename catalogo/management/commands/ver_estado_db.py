from django.core.management.base import BaseCommand
from catalogo.models import Categoria, Libro

class Command(BaseCommand):
    help = 'Muestra el estado actual de la base de datos'

    def handle(self, *args, **kwargs):
        # Verificar categorías
        categorias = Categoria.objects.all()
        self.stdout.write(self.style.SUCCESS(f'Total de categorías: {categorias.count()}'))
        
        for categoria in categorias:
            self.stdout.write(self.style.SUCCESS(f'\nCategoría: {categoria.nombre}'))
            self.stdout.write(f'Slug: {categoria.slug}')
            self.stdout.write(f'Descripción: {categoria.descripcion}')
            self.stdout.write(f'Total de libros: {categoria.libros.count()}')
            
            # Mostrar libros de esta categoría
            libros = categoria.libros.all()
            for libro in libros:
                self.stdout.write(f'- {libro.titulo} (ID: {libro.pk})')
        
        # Verificar libros sin categoría
        libros_sin_categoria = Libro.objects.filter(categoria__isnull=True)
        if libros_sin_categoria.exists():
            self.stdout.write(self.style.WARNING('\nLibros sin categoría:'))
            for libro in libros_sin_categoria:
                self.stdout.write(f'- {libro.titulo} (ID: {libro.pk})') 