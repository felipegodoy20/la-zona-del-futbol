from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator

# Create your models here.
class TipoCancha(models.Model):
    nombre = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Tipo de Cancha"
    )
    slug = models.SlugField(
        max_length=120,
        unique=True,
        blank=True,
        help_text="URL amigable"
    )
    descripcion = models.TextField(
        blank=True,
        verbose_name="Descripción"
    )
    activo = models.BooleanField(
        default=True,
        verbose_name="¿Activo?"
    )
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Tipos de Cancha"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)


class Cancha(models.Model):

    ESTADO_CHOICES = [
        ('disponible', 'Disponible'),
        ('mantencion', 'En Mantención'),
        ('reservada', 'Reservada'),
        ('suspendida', 'Suspendida'),
    ]

    codigo = models.CharField(
        max_length=10,
        unique=True,
        verbose_name="Código"
    )
    nombre = models.CharField(
        max_length=200,
        verbose_name="Nombre de la Cancha"
    )
    slug = models.SlugField(
        max_length=220,
        unique=True,
        blank=True
    )
    tipo = models.ForeignKey(
        TipoCancha,
        on_delete=models.PROTECT,
        related_name="canchas",
        verbose_name="Tipo de Cancha"
    )
    superficie = models.CharField(
        max_length=100,
        verbose_name="Superficie"
    )
    dimensiones = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Dimensiones"
    )
    descripcion = models.TextField(
        verbose_name="Descripción y Servicios"
    )
    tarifa_bloque = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        validators=[MinValueValidator(0)],
        verbose_name="Tarifa por bloque (CLP)"
    )
    cupos_bloques = models.PositiveIntegerField(
        default=0,
        verbose_name="Bloques disponibles por jornada"
    )
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='disponible',
        verbose_name="Estado"
    )
    imagen = models.ImageField(
        upload_to="canchas/",
        blank=True,
        null=True,
        verbose_name="Fotografía"
    )
    destacado = models.BooleanField(
        default=False,
        verbose_name="¿Destacada?"
    )
    activo = models.BooleanField(
        default=True,
        verbose_name="¿Vigente?"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Canchas"
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

    @property
    def disponible(self):
        return (
            self.estado == 'disponible'
            and self.cupos_bloques > 0
        )

    @property
    def tarifa_formateada(self):
        return f"${self.tarifa_bloque:,.0f}".replace(",", ".")

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.nombre)
            slug = base_slug
            contador = 1

            while Cancha.objects.filter(
                slug=slug
            ).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{contador}"
                contador += 1

            self.slug = slug

        super().save(*args, **kwargs)
