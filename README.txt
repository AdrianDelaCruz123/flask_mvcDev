# SISTEMA DE GESTION DE BIBLIOTECA (FLASK MVC)

# DESCRIPCION DEL PROYECTO
Aplicacion web desarrollada en Python y Flask para la administracion integral de una biblioteca. El proyecto implementa una arquitectura **MVC (Modelo-Vista-Controlador)** estricta para garantizar un codigo limpio y escalable.

El sistema permite la gestion de socios y libros, controlando el flujo de prestamos mediante reglas de negocio (un socio solo puede tener un libro prestado simultaneamente) y asegurando el acceso mediante un sistema de autenticacion con roles diferenciados (Admin y Usuario).

# INSTRUCCIONES DE EJECUCION

Sigue estos pasos para poner en marcha el proyecto:

1.  Clonar el repositorio o descargar el codigo.

2.  Crear y activar el entorno virtual:
    ```bash
    python -m venv venv
    ```
    Windows: `.\venv\Scripts\activate`

3.  Instalar dependencias:
    El proyecto incluye un archivo con todas las librerias necesarias.
    ```bash
    pip install -r requirements.txt
    ```

4.  Iniciar la aplicacion:
    ```bash
    python run.py
    ```

5.  Acceso:
    Abre tu navegador en `http://127.0.0.1:5000`

# CREDENCIALES DE PRUEBA

El sistema cuenta con usuarios pre-cargados para probar los diferentes roles:

|Administrador| `admin` | `admin123` | Control total |
|Usuario| `usuario` | `1234` | Solo lectura |

# ESTRUCTURA DEL CODIGO

El proyecto sigue una estructura basada en Blueprints:

* `/app`: Carpeta principal de la aplicacion.
    * `/controllers`: Manejan las rutas y las peticiones HTTP.
    * `/models`: Definicion de las tablas de la base de datos.
    * `/services`: Logica de negocio, seguridad y validaciones complejas.
    * `/forms`: Formularios web validados con WTForms.
    * `/templates`: Archivos HTML organizados por modulos.
    * `/static`: Archivos CSS, JavaScript e imagenes.
    * `/utils`: Configuraciones y extensiones globales.
* `/instance`: Contiene la base de datos SQLite.
* `run.py`: Punto de entrada para ejecutar el servidor.

# POSIBLES MEJORAS FUTURAS

Para siguientes versiones del software, se proponen las siguientes implementaciones:

1.  Migracion de Usuarios: Actualmente los usuarios y roles residen en memoria. Lo ideal seria moverlos a la base de datos para permitir el registro de nuevos administradores dinamicamente.
2.  Recuperacion de Contraseña: Implementar sistema de envio de emails para restablecer claves olvidadas.
3.  Historial de Prestamos: Crear una vista donde se puedan consultar los prestamos ya devueltos (historico).

