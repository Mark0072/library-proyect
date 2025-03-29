from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q, Count
from .models import Libro, Categoria
from django.utils.text import slugify
from django.urls import reverse

# Create your views here.

def lista_libros(request):
    query = request.GET.get('q', '')
    if query:
        libros = Libro.objects.filter(
            Q(titulo__icontains=query) |
            Q(autor__icontains=query) |
            Q(descripcion__icontains=query)
        )
    else:
        libros = Libro.objects.all()
    
    return render(request, 'catalogo/lista_libros.html', {
        'libros': libros,
        'query': query
    })

def detalle_libro(request, slug):
    libro = get_object_or_404(Libro, slug=slug)
    libros_relacionados = Libro.objects.filter(categoria=libro.categoria).exclude(id=libro.id)[:3]
    
    context = {
        'libro': libro,
        'libros_relacionados': libros_relacionados,
    }
    return render(request, 'catalogo/libro_detalle.html', context)

def catalogo(request):
    # Obtener todos los libros y categorías
    libros = Libro.objects.all().order_by('titulo')
    categorias = Categoria.objects.all().order_by('nombre')
    
    # Debug: Imprimir información sobre los libros
    print(f"Total de libros: {libros.count()}")
    
    # Asegurar que todos los libros tengan slug
    for libro in libros:
        if not libro.slug:
            base_slug = slugify(libro.titulo)
            slug = base_slug
            counter = 1
            # Asegurar que el slug sea único
            while Libro.objects.filter(slug=slug).exclude(id=libro.id).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            libro.slug = slug
            libro.save()
            print(f"Generado slug para libro {libro.id}: {libro.slug}")
    
    # Filtrado por categoría
    categoria_id = request.GET.get('categoria')
    if categoria_id:
        libros = libros.filter(categoria_id=categoria_id)
        print(f"Filtrado por categoría {categoria_id}: {libros.count()} libros")
    
    # Búsqueda por título o autor
    query = request.GET.get('q')
    if query:
        libros = libros.filter(
            Q(titulo__icontains=query) |
            Q(autor__icontains=query)
        )
        print(f"Búsqueda '{query}': {libros.count()} resultados")
    
    context = {
        'libros': libros,
        'categorias': categorias,
        'query': query,
        'categoria_seleccionada': categoria_id,
    }
    
    # Debug: Verificar el contexto
    print("Contexto:", context)
    
    return render(request, 'catalogo/catalogo.html', context)

def categoria(request, slug):
    categoria = get_object_or_404(Categoria, slug=slug)
    libros = Libro.objects.filter(categoria=categoria).order_by('titulo')
    
    # Búsqueda por título o autor
    query = request.GET.get('q')
    if query:
        libros = libros.filter(titulo__icontains=query) | libros.filter(autor__icontains=query)
    
    context = {
        'categoria': categoria,
        'libros': libros,
        'query': query,
    }
    return render(request, 'catalogo/categoria.html', context)

def lista_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'catalogo/categorias.html', {'categorias': categorias})

def inicio(request):
    total_libros = Libro.objects.count()
    total_categorias = Categoria.objects.count()
    ultimos_libros = Libro.objects.order_by('-fecha_publicacion')[:6]
    
    context = {
        'total_libros': total_libros,
        'total_categorias': total_categorias,
        'ultimos_libros': ultimos_libros,
    }
    return render(request, 'catalogo/inicio.html', context)