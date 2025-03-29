from django.core.management.base import BaseCommand
from django.utils.text import slugify
from catalogo.models import Categoria

class Command(BaseCommand):
    help = 'Crea una nueva categoría'

    def add_arguments(self, parser):
        parser.add_argument('nombre', type=str, help='Nombre de la categoría')
        parser.add_argument('descripcion', type=str, help='Descripción de la categoría')

    def handle(self, *args, **options):
        nombre = options['nombre']
        descripcion = options['descripcion']
        slug = slugify(nombre)

        categoria, created = Categoria.objects.get_or_create(
            nombre=nombre,
            defaults={
                'descripcion': descripcion,
                'slug': slug
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f'Categoría "{nombre}" creada exitosamente'))
        else:
            self.stdout.write(self.style.WARNING(f'La categoría "{nombre}" ya existe')) 