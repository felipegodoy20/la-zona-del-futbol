from django.contrib import admin
from .models import TipoCancha, Cancha
# Register your models here.

admin.site.site_header = "La Zona del Fútbol - Panel de Control"
admin.site.site_title = "La Zona del Fútbol Admin"
admin.site.index_title = "Gestión Operativa de Recursos y Servicios"


@admin.register(TipoCancha)
class TipoCanchaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'slug', 'activo', 'creado_en')
    search_fields = ('nombre', 'descripcion')
    prepopulated_fields = {'slug': ('nombre',)}
    list_editable = ('activo',)


@admin.register(Cancha)
class CanchaAdmin(admin.ModelAdmin):
    list_display = (
        'codigo',
        'nombre',
        'tipo',
        'tarifa_formateada',
        'cupos_bloques',
        'estado',
        'activo',
        'destacado'
    )
    list_filter = ('tipo', 'estado', 'activo', 'destacado')
    search_fields = ('codigo', 'nombre', 'superficie', 'descripcion')
    list_editable = ('cupos_bloques', 'estado', 'activo', 'destacado')
    prepopulated_fields = {'slug': ('nombre',)}
    list_per_page = 15

    # Formulario dividido en secciones lógicas
    fieldsets = (
        ('Identificación', {
            'fields': ('codigo', 'nombre', 'slug', 'tipo')
        }),
        ('Características', {
            'fields': ('superficie', 'dimensiones', 'descripcion', 'imagen')
        }),
        ('Tarifa y disponibilidad', {
            'fields': ('tarifa_bloque', 'cupos_bloques', 'estado')
        }),
        ('Publicación', {
            'fields': ('destacado', 'activo')
        }),
    )
