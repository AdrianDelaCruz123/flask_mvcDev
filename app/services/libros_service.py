from app.extensions import db
from app.models.libro import Libro
from sqlalchemy import or_ 

def listar_libros(busqueda=None):
    query = Libro.query
    
    # si el usuario ha escrito algo en el buscador entramos aqui
    if busqueda:
        # filtro para que busque si el texto esta en el titulo o en el autor
        # si no tienes importado or_ puedes usar solo la linea del titulo
        query = query.filter(
            or_(
                Libro.titulo.contains(busqueda),
                Libro.autor.contains(busqueda)
            )
        )
    
    # devuelve la lista filtrada o completa si no habia busqueda
    return query.all()

def listar_libros_prestados():
    # filtra y devuelve solo los libros que estan prestados a alguien ahora mismo
    return Libro.query.filter(Libro.socio_id != None).all()

def obtener_libro(id):
    # busca un libro por su id y si no existe lanza un error 404 automatico
    return Libro.query.get_or_404(id)

def crear_libro(titulo, autor, resumen):
    # creo el objeto libro nuevo con los datos que me pasan
    nuevo_libro = Libro(titulo=titulo, autor=autor, resumen=resumen)
    # lo preparo para guardar y confirmo el cambio en la db
    db.session.add(nuevo_libro)
    db.session.commit()
    return nuevo_libro

def editar_libro(libro_id, titulo, autor, resumen):
    # primero busco el libro que queremos editar
    libro = Libro.query.get_or_404(libro_id)
    # actualizo las propiedades con los valores nuevos que vienen del formulario
    libro.titulo = titulo
    libro.autor = autor
    libro.resumen = resumen
    # guardo los cambios permanentemente
    db.session.commit()
    return libro

def eliminar_libro(id):
    libro = Libro.query.get(id)
    if libro:
        # si encuentro el libro lo borro de la base de datos
        db.session.delete(libro)
        db.session.commit()
        return True
    return False