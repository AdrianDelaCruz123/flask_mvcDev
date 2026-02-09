from flask import Blueprint, redirect, url_for, flash, request
from flask_login import login_required
from app.services.prestamos_service import prestar_libro_accion, devolver_libro_accion

prestamos_bp = Blueprint('prestamos', __name__, url_prefix='/prestamos')

@prestamos_bp.route('/prestar/<int:libro_id>', methods=['POST'])
@login_required
def prestar(libro_id):
    socio_id = request.form.get('socio_id')
    
    # Validacion basica: si no eligen socio
    if not socio_id:
        flash("Debes seleccionar un socio.", "warning")
        return redirect(url_for('libros.listar'))

    # Llamada al servicio
    resultado = prestar_libro_accion(libro_id, socio_id)
    
    # Gestion de respuestas
    if resultado == "exito":
        flash("Libro prestado correctamente.", 'success')
    elif resultado == "limite_alcanzado":
        flash("No se puede prestar: Este socio ya tiene un libro sin devolver.", 'danger')
    elif resultado == "libro_ocupado":
        flash("El libro ya no está disponible.", 'warning')
    
    return redirect(url_for('libros.listar'))


# Fijate que esta funcion solo aparece una vez aqui
@prestamos_bp.route('/devolver/<int:libro_id>', methods=['POST'])
@login_required
def devolver(libro_id):
    devolver_libro_accion(libro_id)
    flash('Libro devuelto correctamente.', 'success')
    return redirect(url_for('libros.listar'))