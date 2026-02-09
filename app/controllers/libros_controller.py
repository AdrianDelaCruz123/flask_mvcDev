from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.forms.libro_form import LibroForm
from app.services.libros_service import listar_libros, crear_libro, editar_libro, eliminar_libro, obtener_libro
from app.services.socios_service import listar_socios 

# creo el blueprint para agrupar todo lo que tiene que ver con libros
libros_bp = Blueprint('libros', __name__, url_prefix='/libros')

@libros_bp.route('/')
def listar():
    busqueda = request.args.get('busqueda')
    libros = listar_libros(busqueda) 
    socios = listar_socios()
    return render_template('paginas/libros/libros.html', libros=libros, socios=socios)

@libros_bp.route('/crear', methods=['GET', 'POST'])
@login_required 
def crear():
    # protejo la ruta para que solo entre gente logueada
    form = LibroForm()
    # si el formulario se ha enviado y los datos valen
    if form.validate_on_submit():
        # llamo al servicio para que guarde el libro nuevo
        crear_libro(form.titulo.data, form.autor.data, form.resumen.data)
        flash('Libro creado correctamente', 'success')
        return redirect(url_for('libros.listar'))
    # si es get simplemente muestro el formulario vacio
    return render_template('paginas/libros/libro_crear.html', form=form)

@libros_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    # busco el libro que queremos editar por su id
    libro = obtener_libro(id)
    # cargo el formulario rellenando los datos con lo que ya tiene el libro
    form = LibroForm(obj=libro)
    
    if form.validate_on_submit():
        # si cambian algo y le dan a guardar actualizo los datos
        editar_libro(id, form.titulo.data, form.autor.data, form.resumen.data)
        flash('Libro actualizado correctamente', 'success')
        return redirect(url_for('libros.listar'))
        
    # muestro la misma plantilla de crear pero con el titulo cambiado
    return render_template('paginas/libros/libro_crear.html', form=form, titulo="Editar Libro")

@libros_bp.route('/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar(id):
    libro = obtener_libro(id)
    # comprobacion importante si el libro lo tiene un socio no dejo borrarlo
    if libro.socio_id:
        flash('No se puede borrar un libro prestado.', 'danger')
    else:
        # si nadie lo tiene llamo al servicio para borrarlo definitivamente
        eliminar_libro(id)
        flash('Libro eliminado correctamente', 'success')
        
    return redirect(url_for('libros.listar'))