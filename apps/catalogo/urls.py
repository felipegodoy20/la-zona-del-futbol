from django.urls import path
from . import views

app_name = 'catalogo'

urlpatterns = [
    path('', views.cancha_lista, name='lista'),
    path('cancha/<slug:slug>/', views.cancha_detalle, name='detalle'),
    path('gestion/', views.gestion_canchas, name='gestion'),
    path('gestion/nueva/', views.cancha_crear, name='crear'),
    path('gestion/editar/<int:id>/', views.cancha_editar, name='editar'),
    path('gestion/eliminar/<int:id>/', views.cancha_eliminar, name='eliminar'),
]