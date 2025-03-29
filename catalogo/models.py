from django.db import models
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('categoria', args=[self.slug])

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'

class Libro(models.Model):
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, null=True, blank=True)
    autor = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha_publicacion = models.DateField()
    imagen = models.ImageField(upload_to='libros/', null=True, blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='libros')
    isbn = models.CharField(max_length=13, blank=True)
    editorial = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse('detalle_libro', args=[str(self.slug)])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Libro'
        verbose_name_plural = 'Libros'
