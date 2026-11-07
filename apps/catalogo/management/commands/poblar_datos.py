from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.catalogo.models import TipoCancha, Cancha
from apps.usuarios.models import Perfil


class Command(BaseCommand):
    help = "Pobla la base de datos con tipos de cancha, canchas y usuarios de prueba."

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser(
                "admin",
                "admin@lazonadelfutbol.cl",
                "admin"
            )
            self.stdout.write(
                self.style.SUCCESS("Superusuario 'admin' creado.")
            )

        if not User.objects.filter(username="cliente").exists():
            User.objects.create_user(
                "cliente",
                "cliente@lazonadelfutbol.cl",
                "cliente",
                first_name="Cliente",
                last_name="De Prueba"
            )
            self.stdout.write(
                self.style.SUCCESS("Usuario estándar 'cliente' creado.")
            )

        # Perfiles (RUT, teléfono y rol) de los usuarios de prueba
        Perfil.objects.update_or_create(
        usuario=User.objects.get(username="admin"),
        defaults={'rut': '11111111-1', 'telefono': '+56 9 1111 1111', 'rol': 'administrador'},
        )
        Perfil.objects.update_or_create(
        usuario=User.objects.get(username="cliente"),
        defaults={'rut': '22222222-2', 'telefono': '+56 9 2222 2222', 'rol': 'cliente'},
        )
        
        tipos = {
            "Fútbol 5 Techada": "Canchas de fútbol 5 bajo techo, ideales para jugar con lluvia o frío.",
            "Fútbol 5 al Aire Libre": "Canchas de fútbol 5 descubiertas, con iluminación nocturna.",
            "Fútbol 7 Techada": "Canchas de fútbol 7 bajo techo para partidos de mayor formato.",
            "Fútbol 7 al Aire Libre": "Canchas de fútbol 7 descubiertas, con iluminación nocturna.",
        }

        tipo_map = {}

        for nombre, desc in tipos.items():
            tipo, _ = TipoCancha.objects.get_or_create(
                nombre=nombre,
                defaults={'descripcion': desc}
            )
            tipo_map[nombre] = tipo

        # (código, nombre, tipo, dimensiones, tarifa por bloque, bloques por jornada, destacada)
        canchas = [
            ("F5T-01", "Cancha F5 Techada 1", "Fútbol 5 Techada", "25 x 15 m", 20000, 12, True),
            ("F5T-02", "Cancha F5 Techada 2", "Fútbol 5 Techada", "25 x 15 m", 20000, 12, False),
            ("F5A-01", "Cancha F5 Aire Libre 1", "Fútbol 5 al Aire Libre", "25 x 15 m", 15000, 12, True),
            ("F5A-02", "Cancha F5 Aire Libre 2", "Fútbol 5 al Aire Libre", "25 x 15 m", 15000, 12, False),
            ("F7T-01", "Cancha F7 Techada 1", "Fútbol 7 Techada", "50 x 30 m", 27000, 10, True),
            ("F7T-02", "Cancha F7 Techada 2", "Fútbol 7 Techada", "50 x 30 m", 27000, 10, False),
            ("F7A-01", "Cancha F7 Aire Libre 1", "Fútbol 7 al Aire Libre", "50 x 30 m", 23000, 10, True),
            ("F7A-02", "Cancha F7 Aire Libre 2", "Fútbol 7 al Aire Libre", "50 x 30 m", 23000, 10, False),
        ]

        for cod, nom, tipo, dim, tarifa, cupos, dest in canchas:
            Cancha.objects.get_or_create(
                codigo=cod,
                defaults={
                    'nombre': nom,
                    'tipo': tipo_map[tipo],
                    'superficie': 'Pasto sintético',
                    'dimensiones': dim,
                    'descripcion': f"{nom}: pasto sintético de alta calidad, camarines y estacionamiento.",
                    'tarifa_bloque': tarifa,
                    'cupos_bloques': cupos,
                    'estado': 'disponible',
                    'destacado': dest,
                    'activo': True,
                }
            )

        self.stdout.write(
            self.style.SUCCESS("Catálogo poblado exitosamente.")
        )
