from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('catalogo/', views.catalogo, name='catalogo'),
    path('categoria/<slug:slug>/', views.categoria, name='categoria'),
    path('categorias/', views.lista_categorias, name='lista_categorias'),
    path('libro/<slug:slug>/', views.detalle_libro, name='detalle_libro'),
]
