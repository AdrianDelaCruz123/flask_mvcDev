from app.models.libro import Libro
from app.models.socio import Socio
from app.extensions import db 
from sqlalchemy import or_  

def listar_socios():
    return Socio.query.all()

def obtener_socio(id):
    return Socio.query.get_or_404(id)

def buscar_socios_por_nombre_email(texto):
    # Usamos el filter para aplicar filtros a lo que va devolver y lo aplicamos con el or_ despues si cumpe esas condiciones 
    # el .all devolvera todo lo que encuentre si no hay nada pues devuelve una lisrta vacia
    return Socio.query.filter(
        or_(
            Socio.nombre.contains(texto),
            Socio.email.contains(texto)
        )
    ).all()

def contar_libros_pendientes(socio_id):
    # Cuenta cuantos libros tiene este socio prestados
    return Libro.query.filter_by(socio_id=socio_id).count()

def listar_socios_con_prestamos():
    # Filtramos los socios que tienen la relación libro_prestado distinta de None
    return Socio.query.filter(Socio.libro_prestado != None).all()

def crear_socio(nombre, email):
    # Creamos el socio si el email ya existe el controlador debera manejar el error
    nuevo_socio = Socio(nombre=nombre, email=email)
    db.session.add(nuevo_socio)
    db.session.commit()
    return nuevo_socio

def actualizar_socio(id, nombre, email):
    socio = Socio.query.get_or_404(id)
    socio.nombre = nombre
    socio.email = email
    db.session.commit()
    return socio

def eliminar_socio(id):
    socio = Socio.query.get_or_404(id)
    db.session.delete(socio)
    db.session.commit()