from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.forms.socio_form import SocioForm
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
    
    # si el usuario ha escrito algo en el buscador filtro la lista
    if busqueda:
        socios = buscar_socios_por_nombre_email(busqueda)
    else:
        # si no hay busqueda traigo todos los socios que existen
        socios = listar_socios()
        
    return render_template('paginas/socios/socios.html', socios=socios)

@socios_bp.route('/crear', methods=['GET', 'POST'])
@admin_required # uso este decorador para que solo el admin pueda crear gente
def crear():
    form = SocioForm()
    # si el formulario esta bien relleno guardo el nuevo socio
    if form.validate_on_submit():
        crear_socio(form.nombre.data, form.email.data)
        flash('Socio creado correctamente', 'success')
        return redirect(url_for('socios.listar'))
        
    return render_template('paginas/socios/crear.html', form=form)

@socios_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@admin_required
def editar(id):
    # busco al socio por su id para saber a quien vamos a editar
    socio = obtener_socio(id)
    # cargo el formulario con los datos que ya tiene el socio
    form = SocioForm(obj=socio)
    
    if form.validate_on_submit():
        # si cambian datos y guardan actualizo la base de datos
        actualizar_socio(id, form.nombre.data, form.email.data)
        flash('Socio actualizado correctamente', 'success')
        return redirect(url_for('socios.listar'))
        
    return render_template('paginas/socios/editar.html', form=form, socio=socio)

@socios_bp.route('/eliminar/<int:id>', methods=['POST'])
@admin_required
def eliminar(id):
    # miro primero cuantos libros tiene este socio sin devolver
    libros_pendientes = contar_libros_pendientes(id)
    
    # esto es importante si tiene libros prestados no dejo borrarlo
    if libros_pendientes > 0:
        flash(f'Error: No puedes borrar al socio porque tiene {libros_pendientes} libros sin devolver.', 'danger')
    else:
        # si no debe nada entonces si lo elimino del sistema
        eliminar_socio(id)
        flash('Socio eliminado correctamente', 'success')
        
    return redirect(url_for('socios.listar'))