from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from apps.catalogo.models import Cancha

# Create your views here.

def _obtener_carrito(request):
    return request.session.setdefault('carrito', {})


def _calcular_totales(carrito):
    # La tarifa ya incluye IVA: se separa el IVA (19%) del total para el desglose
    total = sum(item['subtotal'] for item in carrito.values())
    iva = round(total * 19 / 119)
    neto = total - iva
    return neto, iva, total


def carrito_ver(request):
    carrito = _obtener_carrito(request)
    neto, iva, total = _calcular_totales(carrito)
    return render(request, 'pedidos/carrito.html', {
        'items_carrito': carrito.values(),
        'subtotal': neto,
        'iva': iva,
        'total': total,
        'esta_vacio': len(carrito) == 0,
    })


def carrito_agregar(request, id):
    cancha = get_object_or_404(Cancha, id=id, activo=True)
    carrito = _obtener_carrito(request)
    str_id = str(cancha.id)

    # Validar disponibilidad antes de agregar
    if cancha.estado != 'disponible':
        messages.warning(request, f"La cancha '{cancha.nombre}' no está disponible ({cancha.get_estado_display()}).")
        return redirect('pedidos:ver')

    cantidad_actual = carrito.get(str_id, {}).get('cantidad', 0)
    nueva_cantidad = cantidad_actual + 1

    # Validar cupos de bloques
    if nueva_cantidad > cancha.cupos_bloques:
        messages.warning(request, f"Límite de bloques alcanzado ({cancha.cupos_bloques}) para '{cancha.nombre}'.")
        return redirect('pedidos:ver')

    imagen_url = cancha.imagen.url if cancha.imagen else ''
    carrito[str_id] = {
        'id': cancha.id,
        'codigo': cancha.codigo,
        'nombre': cancha.nombre,
        'slug': cancha.slug,
        'tipo': cancha.tipo.nombre,
        'precio': int(cancha.tarifa_bloque),
        'cantidad': nueva_cantidad,
        'subtotal': int(cancha.tarifa_bloque) * nueva_cantidad,
        'imagen_url': imagen_url,
    }

    # Notifica a Django que la sesión fue modificada
    request.session.modified = True
    messages.success(request, f"'{cancha.nombre}' añadida a tu reserva.")
    return redirect(request.META.get('HTTP_REFERER') or 'pedidos:ver')


def carrito_restar(request, id):
    carrito = _obtener_carrito(request)
    str_id = str(id)
    if str_id in carrito:
        carrito[str_id]['cantidad'] -= 1
        if carrito[str_id]['cantidad'] <= 0:
            del carrito[str_id]
        else:
            carrito[str_id]['subtotal'] = carrito[str_id]['precio'] * carrito[str_id]['cantidad']
        request.session.modified = True
    return redirect('pedidos:ver')


def carrito_eliminar(request, id):
    carrito = _obtener_carrito(request)
    str_id = str(id)
    if str_id in carrito:
        del carrito[str_id]
        request.session.modified = True
        messages.warning(request, "Cancha eliminada de la reserva.")
    return redirect('pedidos:ver')


def carrito_limpiar(request):
    if 'carrito' in request.session:
        del request.session['carrito']
        request.session.modified = True
    return redirect('pedidos:ver')


@login_required
def checkout_simulado(request):
    carrito = _obtener_carrito(request)
    if not carrito:
        return redirect('catalogo:lista')

    neto, iva, total = _calcular_totales(carrito)
    items_reservados = list(carrito.values())

    # Vista de resumen vacía la sesión
    del request.session['carrito']
    request.session.modified = True

    return render(request, 'pedidos/checkout_exito.html', {
        'items': items_reservados,
        'subtotal': neto,
        'iva': iva,
        'total': total,
        'orden_id': f"RES-{request.user.id}-2026",
    })