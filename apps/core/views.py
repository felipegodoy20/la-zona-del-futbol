from django.shortcuts import render
from apps.catalogo.models import Cancha, TipoCancha
# Create your views here.


def inicio(request):
    destacadas = Cancha.objects.filter(
        activo=True,
        destacado=True
    ).select_related('tipo')[:4]

    tipos = TipoCancha.objects.filter(activo=True)[:6]

    return render(request, 'core/index.html', {
        'destacadas': destacadas,
        'tipos': tipos,
        'total_canchas': Cancha.objects.filter(activo=True).count(),
        'total_tipos': TipoCancha.objects.filter(activo=True).count(),
    })


def nosotros(request):
    return render(request, 'core/nosotros.html')

