from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired

class PrestamoForm(FlaskForm):
    # El SelectField crea un desplegable HTML
    socio_id = SelectField('Selecciona un Socio', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Confirmar Préstamo')