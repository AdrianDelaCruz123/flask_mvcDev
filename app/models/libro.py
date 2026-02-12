from app.extensions import db 

# defino la clase libro que representa la tabla en la base de datos
class Libro(db.Model):
    __tablename__ = 'libros'

    # configuro las columnas de la tabla
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False) 
    autor = db.Column(db.String(100), nullable=False)
    genero = db.Column(db.String(50), nullable=True)
    anio_publicacion = db.Column(db.Integer, nullable=True)
    
    # clave foranea que conecta con la tabla socios para saber quien tiene el libro prestado
    socio_id = db.Column(db.Integer, db.ForeignKey('socios.id'), nullable=True)

    def __repr__(self):
        # esto ayuda a ver el nombre del libro cuando hacemos debug en la consola
        return f'<Libro {self.titulo}>'
    
    @property
    def codigo(self):
        # creo una propiedad extra para llamar codigo al id
        return self.id

    def to_dict(self):
        # convierte el objeto libro en un diccionario json util para la api
        return {
            "id": self.id,
            "codigo": self.codigo,
            "titulo": self.titulo,
            "autor": self.autor,
            # actualizamos tambien el diccionario
            "genero": self.genero,
            "anio_publicacion": self.anio_publicacion,
            "socio_id": self.socio_id,
            # calculo automatico si no tiene socio id es que esta disponible
            "disponible": self.socio_id is None 
        }