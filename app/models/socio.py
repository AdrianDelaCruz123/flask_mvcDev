from app.extensions import db 

class Socio(db.Model):
    __tablename__ = 'socios'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    
    # conecta con el modelo Libro 
    libro_prestado = db.relationship('Libro', backref='socio', uselist=False, lazy=True)

    @property
    def codigo(self):
        return self.id

    def to_dict(self):
        return {
            "id": self.id,
            "codigo": self.codigo,
            "nombre": self.nombre,
            "email": self.email,
            # si tiene libro devolvemos su titulo si no null
            "libro_prestado": self.libro_prestado.titulo if self.libro_prestado else None,
            "libro_id": self.libro_prestado.id if self.libro_prestado else None
        }