from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings
from catalogo.models import Libro
import os
import requests
from urllib.parse import urlparse

class Command(BaseCommand):
    help = 'Agrega imágenes de ejemplo a los libros'

    def handle(self, *args, **options):
        # URLs de imágenes de ejemplo por libro
        imagenes_libros = {
            'HABIT ATOMICS': 'https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?w=500',
            'Rich Dad Poor Dad': 'https://images.unsplash.com/photo-1543002580-b0de87a0d96d?w=500',
            'The 48 Laws of Power': 'https://images.unsplash.com/photo-1541963463532-d68292c34b19?w=500',
        }

        # URLs de imágenes por categoría (para libros nuevos)
        imagenes_categorias = {
            'self-help': 'https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?w=500',
            'fiction': 'https://images.unsplash.com/photo-1543002580-b0de87a0d96d?w=500',
            'non-fiction': 'https://images.unsplash.com/photo-1541963463532-d68292c34b19?w=500',
        }

        for libro in Libro.objects.all():
            if not libro.imagen:
                # Intentar obtener una imagen específica para el libro
                url_imagen = imagenes_libros.get(libro.titulo)
                
                # Si no hay imagen específica, usar la de la categoría
                if not url_imagen:
                    categoria = libro.categoria.slug if libro.categoria else 'non-fiction'
                    url_imagen = imagenes_categorias.get(categoria, imagenes_categorias['non-fiction'])
                
                try:
                    # Descargar la imagen
                    response = requests.get(url_imagen)
                    if response.status_code == 200:
                        # Obtener el nombre del archivo de la URL
                        nombre_archivo = os.path.basename(urlparse(url_imagen).path)
                        if not nombre_archivo:
                            nombre_archivo = f'libro_{libro.id}.jpg'
                        
                        # Guardar la imagen
                        ruta_imagen = os.path.join(settings.MEDIA_ROOT, 'libros', nombre_archivo)
                        os.makedirs(os.path.dirname(ruta_imagen), exist_ok=True)
                        
                        with open(ruta_imagen, 'wb') as f:
                            f.write(response.content)
                        
                        # Asignar la imagen al libro
                        with open(ruta_imagen, 'rb') as f:
                            libro.imagen.save(nombre_archivo, File(f), save=True)
                        
                        self.stdout.write(self.style.SUCCESS(f'Imagen agregada al libro "{libro.titulo}"'))
                    else:
                        self.stdout.write(self.style.ERROR(f'Error al descargar imagen para "{libro.titulo}"'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error al procesar imagen para "{libro.titulo}": {str(e)}'))
            else:
                self.stdout.write(self.style.WARNING(f'El libro "{libro.titulo}" ya tiene una imagen')) 