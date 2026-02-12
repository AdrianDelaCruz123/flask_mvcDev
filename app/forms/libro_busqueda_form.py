from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Optional

class LibroBusquedaForm(FlaskForm):
    busqueda = StringField('', validators=[Optional()])
    submit = SubmitField('Buscar')