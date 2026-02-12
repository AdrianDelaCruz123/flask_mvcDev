from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.forms.socio_form import SocioForm
from app.models.socio import Socio
from app.services.socios_service import (
    listar_socios, 
    buscar_socios_por_nombre_email, 
    crear_socio, 
    obtener_socio, 
    actualizar_socio, 
    eliminar_socio,
    contar_libros_pendientes
)
from app.utils.decorators import admin_required

# creo el blueprint para manejar todas las rutas de la gestion de socios
socios_bp = Blueprint('socios', __name__, url_prefix='/socios')

@socios_bp.route('/')
def listar():
    busqueda = request.args.get('busqueda')
    solo_prestamos = request.args.get('solo_prestamos') 

    if solo_prestamos:
        socios = [s for s in listar_socios() if s.libro_prestado]
    elif busqueda:
        socios = buscar_socios_por_nombre_email(busqueda)
    else:
        socios = listar_socios()
        
    return render_template('paginas/socios/socios.html', socios=socios)
@socios_bp.route('/crear', methods=['GET', 'POST'])
@admin_required
def crear():
    form = SocioForm()
    if form.validate_on_submit():
        existente = Socio.query.filter_by(email=form.email.data).first()
        if existente:
            flash(f'El email {form.email.data} ya está registrado.', 'danger')
            return render_template('paginas/socios/crear.html', form=form, titulo="Nuevo Socio")

        crear_socio(form.nombre.data, form.email.data)
        flash('Socio creado correctamente', 'success')
        return redirect(url_for('socios.listar'))
        
    return render_template('paginas/socios/crear.html', form=form, titulo="Nuevo Socio")

@socios_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@admin_required
def editar(id):
    socio = obtener_socio(id)
    form = SocioForm(obj=socio)
    
    if form.validate_on_submit():
        otro_con_mismo_email = Socio.query.filter(Socio.email == form.email.data, Socio.id != id).first()
        if otro_con_mismo_email:
            flash('Error: Ese email ya pertenece a otro socio.', 'danger')
            return render_template('paginas/socios/crear.html', form=form, titulo="Editar Socio")

        actualizar_socio(id, form.nombre.data, form.email.data)
        flash('Socio actualizado correctamente', 'success')
        return redirect(url_for('socios.listar'))
        
    return render_template('paginas/socios/crear.html', form=form, titulo="Editar Socio")

@socios_bp.route('/eliminar/<int:id>', methods=['POST'])
@admin_required
def eliminar(id):
    # miro primero cuantos libros tiene este socio sin devolver
    libros_pendientes = contar_libros_pendientes(id)
    
    # esto es importante si tiene libros prestados no dejo borrarlo
    if libros_pendientes > 0:
        flash(f'Error: No puedes borrar al socio porque tiene {libros_pendientes} libro(s) sin devolver.', 'danger')
    else:
        # si no debe nada entonces si lo elimino del sistema
        eliminar_socio(id)
        flash('Socio eliminado correctamente', 'success')
        
    return redirect(url_for('socios.listar'))