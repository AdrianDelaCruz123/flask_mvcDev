from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

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
        validators=[DataRequired(), Length(max=100)]
    )

    resumen = TextAreaField(
        "Resumen",
        # uso textarea porque el resumen ocupa mas espacio y pido un minimo de 5 letras
        validators=[Length(min=5, max=1000)]

    )

    # el boton para guardar todo lo que han escrito
    submit = SubmitField("Guardar")