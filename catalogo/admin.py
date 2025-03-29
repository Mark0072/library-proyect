from django.contrib import admin
from django.core.files import File
from django.conf import settings
from django.utils.html import format_html
from django import forms
from .models import Libro, Categoria
import requests
from urllib.parse import urlparse
import os

class LibroAdminForm(forms.ModelForm):
    imagen_url = forms.URLField(
        required=False,
        label='URL de la imagen',
        help_text='Ingresa una URL de imagen para descargarla automáticamente'
    )

    class Meta:
        model = Libro
        fields = '__all__'

class LibroAdmin(admin.ModelAdmin):
    form = LibroAdminForm
    list_display = ('titulo', 'autor', 'categoria', 'fecha_publicacion', 'imagen_preview')
    list_filter = ('categoria', 'autor')
    search_fields = ('titulo', 'autor', 'descripcion')
    readonly_fields = ('imagen_preview',)
    fields = ('titulo', 'autor', 'descripcion', 'fecha_publicacion', 'categoria', 'imagen_url', 'imagen', 'imagen_preview')
    
    def imagen_preview(self, obj):
        if obj.imagen:
            return format_html('<img src="{}" style="max-height: 50px;"/>', obj.imagen.url)
        return "No hay imagen"
    imagen_preview.short_description = 'Vista previa'

    def save_model(self, request, obj, form, change):
        # Si se proporciona una URL de imagen
        if 'imagen_url' in form.cleaned_data and form.cleaned_data['imagen_url']:
            url = form.cleaned_data['imagen_url']
            try:
                # Descargar la imagen
                response = requests.get(url)
                if response.status_code == 200:
                    # Obtener el nombre del archivo
                    nombre_archivo = os.path.basename(urlparse(url).path)
                    if not nombre_archivo:
                        nombre_archivo = f'libro_{obj.id}.jpg'
                    
                    # Guardar la imagen
                    ruta_imagen = os.path.join(settings.MEDIA_ROOT, 'libros', nombre_archivo)
                    os.makedirs(os.path.dirname(ruta_imagen), exist_ok=True)
                    
                    with open(ruta_imagen, 'wb') as f:
                        f.write(response.content)
                    
                    # Asignar la imagen al libro
                    with open(ruta_imagen, 'rb') as f:
                        obj.imagen.save(nombre_archivo, File(f), save=False)
            except Exception as e:
                self.message_user(request, f'Error al descargar la imagen: {str(e)}', level='ERROR')
        
        super().save_model(request, obj, form, change)

# Register your models here.
admin.site.register(Libro, LibroAdmin)
admin.site.register(Categoria)
