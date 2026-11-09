# La Zona del Fútbol – Chillán

> Donde comienza la pasión.

Sistema web de reservas para un complejo deportivo de fútbol, desarrollado con Django y Bootstrap 5 para la Evaluación Sumativa N°3 de Programación Back End (Sección: N4-P1-C1), Unidad 2: Framework Back End.

## Ficha de Registro

| Campo | Detalle |
|---|---|
| Nombre de la Organización o Plataforma | La Zona del Fútbol |
| Modelo de Negocio / Giro | Complejo deportivo con arriendo de canchas de fútbol 5 y fútbol 7, techadas y al aire libre |
| Integrante| [Felipe Ignacio Godoy Ponce] – Rut [21.604.341-3]  
| Correo institucional | [felipe.godoy32@inacapmail.cl] |
| Entidad de Contexto / Agrupación (ORM) | `TipoCancha` |
| Entidad Principal Gestionable (ORM) | `Cancha` |
| Propósito de la Sesión (`request.session`) | Reserva de jornada por bloques de 1 hora (18:00 a 00:00, máximo 6 por cancha), con tarifa IVA incluido y desglose de neto, IVA (19%) y total |

## Funcionalidades

- **Catálogo público** con tarjetas Bootstrap, búsqueda multicampo con `Q` (código, nombre, descripción, superficie y tipo), filtro por tipo de cancha, ordenamiento por tarifa y paginación con `Paginator`. Cada cancha tiene su ficha, accesible por `slug`.
- **Reserva en sesión** (`request.session`): agregar, sumar y restar bloques, quitar una cancha y vaciar la reserva. Valida el estado de la cancha y el máximo de bloques por jornada. Muestra el desglose de neto, IVA y total, y un comprobante simulado que vacía la sesión. El contador del navbar se inyecta con un *context processor*.
- **Backoffice protegido por rol** (`@login_required` y `@user_passes_test` con `is_staff`): CRUD completo de canchas, con formulario Bootstrap, subida de imágenes (`request.FILES`), validaciones `clean_()` y pantalla de confirmación antes de eliminar.
- **Django Admin personalizado**: títulos corporativos, `list_display`, `list_filter`, `search_fields`, `list_editable` y `fieldsets`.
- **Usuarios**: registro, login y logout, con perfil (RUT validado con dígito verificador, teléfono y rol institucional). Todos los formularios POST llevan `{% csrf_token %}`.

## Reglas de negocio

- Horario de atención: 18:00 a 00:00, en 6 bloques de 1 hora (18:00-19:00, 19:00-20:00, 20:00-21:00, 21:00-22:00, 22:00-23:00 y 23:00-00:00).
- La tarifa por bloque es el **precio final con IVA incluido**. El desglose separa el IVA dentro del total:
  `IVA = total × 19 / 119` y `neto = total − IVA`.
  Ejemplo: 1 bloque de $20.000 → neto $16.807, IVA $3.193, total $20.000.

| Tipo de cancha | Tarifa por bloque (IVA incluido) |
|---|---|
| Fútbol 5 Techada | $20.000 |
| Fútbol 5 al Aire Libre | $15.000 |
| Fútbol 7 Techada | $27.000 |
| Fútbol 7 al Aire Libre | $23.000 |

## Tecnologías

Python 3.12 o superior (probado con 3.13), Django 6.1, Pillow, python-dotenv, SQLite, Bootstrap 5.3 y Bootstrap Icons. Las versiones exactas están fijadas en `requirements.txt`.

## Estructura del proyecto

```
la-zona-del-futbol/
├── apps/
│   ├── catalogo/    modelos TipoCancha y Cancha, formularios, CRUD, admin y comando poblar_datos
│   ├── core/        portada y página "Quiénes Somos"
│   ├── pedidos/     reserva en sesión y context processor
│   └── usuarios/    registro, login, logout y perfil
├── config/          configuración del proyecto (settings, urls)
├── templates/       plantillas base y por aplicación
├── .env.example     ejemplo de variables de entorno
├── manage.py
└── requirements.txt
```

## Instalación paso a paso

Los comandos son para Windows PowerShell.

1. Clonar el repositorio:
   ```powershell
   git clone https://github.com/felipegodoy20/la-zona-del-futbol.git
   cd la-zona-del-futbol
   ```
2. Crear y activar el entorno virtual:
   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```
3. Instalar las dependencias:
   ```powershell
   pip install -r requirements.txt
   ```
4. Crear el archivo `.env` a partir del ejemplo:
   ```powershell
   Copy-Item .env.example .env
   ```
5. (Recomendado) Generar una clave secreta nueva y pegarla en `SECRET_KEY` dentro de `.env`, entre comillas simples:
   ```powershell
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```
6. Crear la base de datos y cargar los datos de prueba:
   ```powershell
   python manage.py migrate
   python manage.py poblar_datos
   ```
7. Iniciar el servidor:
   ```powershell
   python manage.py runserver
   ```
8. Abrir `http://127.0.0.1:8000/`.

El comando `poblar_datos` carga 4 tipos de cancha, 8 canchas y 2 usuarios de prueba. Se puede ejecutar varias veces sin duplicar datos.

## Credenciales de prueba

| Rol | Usuario | Contraseña |
|---|---|---|
| Administrador (staff) | `admin` | `admin` |
| Cliente | `cliente` | `cliente` |

| Sección | Dirección |
|---|---|
| Catálogo | `http://127.0.0.1:8000/catalogo/` |
| Mi reserva | `http://127.0.0.1:8000/pedidos/carrito/` |
| Registro | `http://127.0.0.1:8000/usuarios/registro/` |
| Gestión de canchas (solo staff) | `http://127.0.0.1:8000/catalogo/gestion/` |
| Django Admin | `http://127.0.0.1:8000/admin/` |

Las fotografías de las canchas no se incluyen en el repositorio (la carpeta `media/` está excluida), por lo que las canchas se muestran sin imagen hasta que se suban. Se pueden cargar desde el panel de gestión (botón de editar) o desde el Django Admin.

## Bitácora de Prompts de IA

Herramientas utilizadas: Claude y ChatGPT, como apoyo para arquitectura ORM, seguridad y lógica de sesión. Todo el código fue revisado, probado y adaptado.

### Caso 1: Arquitectura y modelado ORM

- **Prompt:** Entregué la pauta de la evaluación y la guía del profesor ("Proyecto Ejemplo Django BD"), con mi tema, un complejo deportivo de fútbol con 4 tipos de cancha y 8 canchas, y pedí que me guiara paso a paso, sin inventar cosas fuera de la guía y la pauta.
- **Respuesta técnica:** Propuso adaptar la guía así: `Categoria` pasa a `TipoCancha`, `Figura` pasa a `Cancha`, `precio` a `tarifa_bloque` y `stock` a `cupos_bloques`. Mantuvo `ForeignKey` con `on_delete=PROTECT` y `MinValueValidator`, y marcó qué elementos venían de la pauta y no de la guía: código único, estado con `choices` y baja lógica con el campo `activo`.
- **Adaptación aplicada:** Revisé el modelo contra la rúbrica y completé el `verbose_name` de `cupos_bloques`. Ajusté las tarifas por tipo de cancha a valores realistas para Chillán y fijé el horario de atención de 18:00 a 00:00 en 6 bloques por jornada.

### Caso 2: Seguridad y variables de entorno

- **Prompt:** Pegué la salida de `git status`, que mostraba `.env` entre los archivos sin seguimiento, y el contenido del `.gitignore`. Después pregunté si podía hacer `git add .` sabiendo que mi clave estaba en el `.env`, y si al estar excluido no se subiría a GitHub.
- **Respuesta técnica:** Detectó que la línea `.env/` del `.gitignore` (con barra final) solo ignora carpetas y no el archivo, por lo que habría subido la clave a un repositorio público. Indicó corregirla a `.env`, verificar con `git check-ignore -v .env` y revisar `git status` antes de confirmar.
- **Adaptación aplicada:** Corregí la línea, verifiqué que `.env` ya no aparecía y publiqué solo `.env.example`, con un valor de relleno y sin la clave real. Además, `requirements.txt` estaba en UTF-16 por la redirección de PowerShell, así que lo regeneré en ASCII.

### Caso 3: Reserva en sesión y cálculo de IVA

- **Prompt:** Pedí que, al momento de pagar, el sistema dijera "IVA incluido" para dejar un precio exacto, porque al escoger la cancha se le sumaba el 19% encima de la tarifa.
- **Respuesta técnica:** Propuso tratar la tarifa como precio final y separar el IVA dentro del total con una función `_calcular_totales`: `iva = round(total × 19 / 119)` y `neto = total − iva`. Los nombres de las variables del contexto no cambian, y solo se actualizan los textos de las plantillas.
- **Adaptación aplicada:** Apliqué la función en la vista de la reserva y en el comprobante, y cambié los textos a "IVA incluido". Verifiqué en el navegador: 1 bloque de $20.000 muestra neto $16.807, IVA $3.193 y total $20.000.