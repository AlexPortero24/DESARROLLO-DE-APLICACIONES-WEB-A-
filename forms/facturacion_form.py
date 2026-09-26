from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class FacturacionForm(FlaskForm):

    numero = StringField(
        "Número de factura",
        validators=[
            DataRequired(message="El número de factura es obligatorio.")
        ]
    )

    cliente = StringField(
        "Cliente",
        validators=[
            DataRequired(message="El cliente es obligatorio.")
        ]
    )

    fecha = StringField(
        "Fecha",
        validators=[
            DataRequired(message="La fecha es obligatoria.")
        ]
    )

    total = FloatField(
        "Total",
        validators=[
            DataRequired(message="El total es obligatorio."),
            NumberRange(
                min=0.01,
                message="El total debe ser mayor que 0."
            )
        ]
    )

    submit = SubmitField("Guardar factura")