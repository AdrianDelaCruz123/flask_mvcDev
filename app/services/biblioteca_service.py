from app.extensions import db 
from app.models.libro import Libro
from app.models.socio import Socio

class BibliotecaService:
    
    def obtener_todos_libros_raw(self):
        # recupero todos los libros de la base de datos tal cual estan
        return Libro.query.all()

    def get_all_socios(self):
        # recupero todos los socios registrados
        return Socio.query.all()

    def procesar_prestamo(self, libro_id, socio_id):
        # busco primero el libro y el socio en la base de datos
        libro = Libro.query.get(libro_id)
        socio = Socio.query.get(socio_id)

        # validacion basica si alguno no existe corto aqui
        if not libro or not socio:
            return False, "Libro o Socio no encontrados."
        
        # compruebo si el libro ya lo tiene otra persona
        if libro.socio_id is not None:
            return False, "El libro ya está prestado."
        
        # compruebo si este socio ya tiene un libro sin devolver porque solo permitimos uno a la vez
        prestamo_actual = Libro.query.filter_by(socio_id=socio.id).first()
        if prestamo_actual:
            return False, f"El socio ya tiene el libro '{prestamo_actual.titulo}'."

        # si todo esta bien asigno el libro al socio
        libro.socio_id = socio.id
        
        try:
            # confirmo los cambios en la base de datos
            db.session.commit() 
            return True, "Préstamo realizado exitosamente."
        except Exception as e:
            # si falla algo deshago los cambios para no dejar datos corruptos
            db.session.rollback()
            return False, f"Error en base de datos: {str(e)}"

    def procesar_devolucion(self, libro_id):
        libro = Libro.query.get(libro_id)

        if not libro:
            return False, "Libro no encontrado."
        
        # verifico que el libro realmente estuviera prestado antes de devolverlo
        if libro.socio_id is None:
            return False, "Este libro no estaba prestado."

        # libero el libro poniendo el socio a none
        libro.socio_id = None

        try:
            db.session.commit()
            return True, "Libro devuelto correctamente."
        except Exception as e:
            db.session.rollback()
            return False, str(e)