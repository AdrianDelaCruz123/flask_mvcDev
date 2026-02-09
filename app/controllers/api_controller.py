from flask import Blueprint, jsonify, request
from app.services.libros_service import listar_libros, listar_libros_prestados
from app.services.socios_service import obtener_socio
from app.utils.decorators import admin_required

api_bp = Blueprint(
    "api",
    __name__,       
    url_prefix="/api"
)

# Listar todos los libros
@api_bp.route("/libros", methods=["GET"])
def listar():
    libros = listar_libros()
    return jsonify([l.to_dict() for l in libros])

# Listar los libros disponibles
@api_bp.route("/libros/disponibles", methods=["GET"])
def disponibles():
    libros = listar_libros()
    # Logica de filtrado en Python 
    libros_disponibles = [l for l in libros if l.socio_id is None]
    return jsonify([l.to_dict() for l in libros_disponibles])

# Buscar un libro por titulo
@api_bp.route("/libros/buscar/<string:titulo>", methods=["GET"])
def buscar(titulo):
    libros = listar_libros()
    encontrados = [l for l in libros if titulo.lower() in l.titulo.lower()]
    return jsonify([l.to_dict() for l in encontrados])

# Ver los lo socios con prestamos
@api_bp.route("/libros/socios/prestamos", methods=["GET"])
@admin_required 
def informe_prestamos():
    # Usamos el servicio de socios_service.py
    libros_prestados = listar_libros_prestados()
    
    lista_prestamos = []
    for libro in libros_prestados:
        # Usamos el servicio de socios_service.py
        socio = obtener_socio(libro.socio_id)
        
        if socio:
            datos = {
                "titulo_libro": libro.titulo,
                "autor_libro": libro.autor,
                "id_socio": socio.id,
                "nombre_socio": socio.nombre,
            }
            lista_prestamos.append(datos)
            
    return jsonify(lista_prestamos)