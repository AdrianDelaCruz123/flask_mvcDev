from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.forms.libro_form import LibroForm
from app.services.libros_service import listar_libros, crear_libro, editar_libro, eliminar_libro, obtener_libro
from app.services.socios_service import listar_socios 
from app.utils.decorators import admin_required 

libros_bp = Blueprint('libros', __name__, url_prefix='/libros')

@libros_bp.route('/')
def listar():
    busqueda = request.args.get('busqueda')
    libros = listar_libros(busqueda) 
    socios = listar_socios()
    return render_template('paginas/libros/libros.html', libros=libros, socios=socios)

@libros_bp.route('/crear', methods=['GET', 'POST'])
@login_required
@admin_required 
def crear():
    form = LibroForm()
    
    if form.validate_on_submit():
        crear_libro(
            titulo=form.titulo.data, 
            autor=form.autor.data, 
            genero=form.genero.data,
            anio_publicacion=form.anio_publicacion.data
        )
        flash('Libro creado correctamente', 'success')
        return redirect(url_for('libros.listar'))
    
    return render_template('paginas/libros/libro_crear.html', form=form, titulo="Nuevo Libro")

@libros_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required 
def editar(id):
    libro = obtener_libro(id)
    form = LibroForm(obj=libro)
    
    if form.validate_on_submit():
        editar_libro(
            libro_id=id, 
            titulo=form.titulo.data, 
            autor=form.autor.data, 
            genero=form.genero.data,
            anio_publicacion=form.anio_publicacion.data
        )
        flash('Libro actualizado correctamente', 'success')
        return redirect(url_for('libros.listar'))
        
    return render_template('paginas/libros/libro_crear.html', form=form, titulo="Editar Libro")

@libros_bp.route('/eliminar/<int:id>', methods=['POST'])
@login_required
@admin_required 
def eliminar(id):
    libro = obtener_libro(id) 

    if libro.socio_id:
        flash("No puedes eliminar un libro que está prestado.", "danger")
        return redirect(url_for('libros.listar'))
        
    eliminar_libro(id)
    flash("Libro eliminado correctamente.", "success")
    return redirect(url_for('libros.listar'))