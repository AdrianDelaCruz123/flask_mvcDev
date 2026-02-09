from flask import Blueprint, render_template
from flask_login import current_user


# creo el blueprint navigation que se encarga de las rutas generales
navigation_bp = Blueprint(
    "navigation",
    __name__,
    url_prefix="/"
)

@navigation_bp.route("/")
def home():
    # esta funcion solo renderiza la pagina de inicio
    return render_template("paginas/inicio.html")