from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Cancha, TipoCancha
from .forms import CanchaForm

# Create your views here.

def es_administrador(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)


def cancha_lista(request):
    query = request.GET.get('q', '').strip()
    tipo_slug = request.GET.get('tipo', '')
    orden = request.GET.get('orden', 'recientes')

    canchas = Cancha.objects.filter(activo=True).select_related('tipo')

    if tipo_slug:
        canchas = canchas.filter(tipo__slug=tipo_slug)

    # Búsqueda multicampo con Q: código, nombre, descripción, superficie y tipo
    if query:
        canchas = canchas.filter(
            Q(codigo__icontains=query) |
            Q(nombre__icontains=query) |
            Q(descripcion__icontains=query) |
            Q(superficie__icontains=query) |
            Q(tipo__nombre__icontains=query)
        )

    ordenes_validos = {
        'precio_asc': 'tarifa_bloque',
        'precio_desc': '-tarifa_bloque',
        'nombre_asc': 'nombre',
        'recientes': '-fecha_creacion',
    }
    canchas = canchas.order_by(ordenes_validos.get(orden, '-fecha_creacion'))

    paginador = Paginator(canchas, 6)
    pagina = paginador.get_page(request.GET.get('page'))
    tipos = TipoCancha.objects.filter(activo=True)

    return render(request, 'catalogo/cancha_lista.html', {
        'canchas': pagina,
        'tipos': tipos,
        'tipo_seleccionado': tipo_slug,
        'query_actual': query,
        'orden_actual': orden,
        'total_resultados': canchas.count(),
    })


def cancha_detalle(request, slug):
    cancha = get_object_or_404(Cancha.objects.select_related('tipo'), slug=slug, activo=True)
    relacionadas = Cancha.objects.filter(tipo=cancha.tipo, activo=True).exclude(pk=cancha.pk)[:3]
    return render(request, 'catalogo/cancha_detalle.html', {'cancha': cancha, 'relacionadas': relacionadas})


@login_required
@user_passes_test(es_administrador, login_url='catalogo:lista')
def gestion_canchas(request):
    query = request.GET.get('q', '').strip()
    canchas = Cancha.objects.all().select_related('tipo')
    if query:
        canchas = canchas.filter(
            Q(codigo__icontains=query) | Q(nombre__icontains=query) | Q(superficie__icontains=query)
        )
    paginador = Paginator(canchas.order_by('-fecha_creacion'), 10)
    pagina = paginador.get_page(request.GET.get('page'))
    return render(request, 'catalogo/gestion_canchas.html', {'canchas': pagina, 'query': query})


@login_required
@user_passes_test(es_administrador, login_url='catalogo:lista')
def cancha_crear(request):
    if request.method == 'POST':
        form = CanchaForm(request.POST, request.FILES)
        if form.is_valid():
            cancha = form.save()
            messages.success(request, f"¡Cancha '{cancha.nombre}' creada exitosamente!")
            return redirect('catalogo:gestion')
    else:
        form = CanchaForm()
    return render(request, 'catalogo/cancha_form.html', {'form': form, 'titulo_accion': 'Ingresar Nueva Cancha', 'boton_texto': 'Guardar'})


@login_required
@user_passes_test(es_administrador, login_url='catalogo:lista')
def cancha_editar(request, id):
    cancha = get_object_or_404(Cancha, id=id)
    if request.method == 'POST':
        form = CanchaForm(request.POST, request.FILES, instance=cancha)
        if form.is_valid():
            form.save()
            messages.success(request, f"Cancha '{cancha.nombre}' actualizada.")
            return redirect('catalogo:gestion')
    else:
        form = CanchaForm(instance=cancha)
    return render(request, 'catalogo/cancha_form.html', {'form': form, 'cancha': cancha, 'titulo_accion': 'Editar Cancha', 'boton_texto': 'Actualizar'})


@login_required
@user_passes_test(es_administrador, login_url='catalogo:lista')
def cancha_eliminar(request, id):
    cancha = get_object_or_404(Cancha, id=id)
    if request.method == 'POST':
        nombre = cancha.nombre
        cancha.delete()
        messages.success(request, f"Cancha '{nombre}' eliminada.")
        return redirect('catalogo:gestion')
    return render(request, 'catalogo/cancha_confirmar_eliminar.html', {'cancha': cancha}) 
