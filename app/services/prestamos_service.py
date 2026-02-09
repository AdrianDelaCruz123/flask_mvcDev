from app.models.libro import Libro
from app.extensions import db

def prestar_libro_accion(libro_id, socio_id):
    libro = Libro.query.get_or_404(libro_id)
    
    # Si el libro ya tiene dueño, error.
    if libro.socio_id is not None:
        return "libro_ocupado"
        
    # Contamos cuántos libros tiene este socio
    cantidad_libros = Libro.query.filter_by(socio_id=socio_id).count()
    
    if cantidad_libros >= 1:
        # Si ya tiene 1, devolvemos este código de error
        return "limite_alcanzado"

    #prestamos
    libro.socio_id = socio_id
    db.session.commit()
    return "exito"

def devolver_libro_accion(libro_id):
    libro = Libro.query.get_or_404(libro_id)
    
    libro.socio_id = None
    db.session.commit()
    return True