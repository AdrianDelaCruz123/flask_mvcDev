from app.models.libro import Libro
from app.models.socio import Socio
from app.extensions import db 


def listar_socios():
    return Socio.query.all()

def obtener_socio(id):
    return Socio.query.get_or_404(id)

def buscar_socios_por_nombre_email(texto):
    # Busca texto dentro del nombre O del email
    return Socio.query.filter(
            (Socio.nombre.ilike(f'%{texto}%')) | 
            (Socio.email.ilike(f'%{texto}%'))
        ).all()

def contar_libros_pendientes(socio_id):
    # Cuenta cuantos libros tiene prestados este socio ahora mismo
    return Libro.query.filter_by(socio_id=socio_id).count()


def crear_socio(nombre, email):
    # No pedimos ID, la base de datos lo pone sola (Autoincrement)
    nuevo_socio = Socio(nombre=nombre, email=email)
    db.session.add(nuevo_socio)
    db.session.commit()
    return nuevo_socio

def actualizar_socio(id, nombre, email):
    socio = Socio.query.get_or_404(id)
    socio.nombre = nombre
    socio.email = email
    db.session.commit()

def eliminar_socio(id):
    socio = Socio.query.get_or_404(id)
    db.session.delete(socio)
    db.session.commit()