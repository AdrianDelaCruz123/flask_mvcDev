from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange

# defino la clase del formulario heredando de flaskform para que sea mas facil
class LibroForm(FlaskForm):
    titulo = StringField(
        "Título",
        # el titulo es obligatorio y pongo un limite de caracteres para que no se pasen
        validators=[DataRequired(message="El título es obligatorio"), Length(max=200)]
    )

    autor = StringField(
        "Autor",
        # el autor tambien tiene que estar relleno si o si
        validators=[DataRequired(message="El autor es obligatorio"), Length(max=100)]
    )

    genero = StringField(
        "Género",
        validators=[DataRequired(message="El género es obligatorio"), Length(max=50)]
    )

    anio_publicacion = IntegerField(
        "Año de Publicación",
        validators=[
            DataRequired(message="El año es obligatorio"),
            # validamos que sea un año positivo 
            NumberRange(min=0, max=2100, message="Introduce un año válido")
        ]
    )

    # el boton para guardar todo lo que han escrito
    submit = SubmitField("Guardar")