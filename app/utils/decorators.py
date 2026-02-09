from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user

# Esta es la funcion principal del decorador recibe la funcion f que queremos proteger
def admin_required(f):
    
    # wraps sirve para copiar la info de la funcion original f
    @wraps(f)
    def decorated_function(*args, **kwargs):
        

        # Si no esta autenticado 
        # O si esta autenticado pero su rol NO es admin
        if not current_user.is_authenticated or current_user.role != 'admin':
            
            # Si se cumple lo de arriba es que no tiene permiso
            # Le mostramos un mensaje de error rojo 
            flash("Acceso denegado. Se requieren permisos de administrador.", "danger")
            
            # Y lo echamos fuera redirigiendolo al login
            return redirect(url_for('auth.login'))
            
        # Si el if de arriba no se cumple significa que es admin asi que dejamos pasar y ejecutamos la funcion original f
        # Los *args y **kwargs son para pasarle los datos que necesite la funcion
        return f(*args, **kwargs)
        
    # Devolvemos la funcion nueva que ya tiene la proteccion incluida
    return decorated_function