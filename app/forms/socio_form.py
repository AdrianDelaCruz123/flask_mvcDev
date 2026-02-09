from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email

class SocioForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    # El validador Email() se asegura de que tenga formato usuario@dominio.com
    email = StringField('Email', validators=[DataRequired(), Email("este formato no mola")])
    submit = SubmitField('Guardar')