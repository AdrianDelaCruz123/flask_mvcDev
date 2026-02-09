from app.extensions import db 

class Socio(db.Model):
    __tablename__ = 'socios'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    
    libro_prestado = db.relationship('Libro', backref='socio_actual', uselist=False, lazy=True)

    @property
    def codigo(self):
        return self.id