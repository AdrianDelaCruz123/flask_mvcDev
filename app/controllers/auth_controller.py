from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from app.services.auth_service import check_credentials

# defino el blueprint auth para separar todo lo que tiene que ver con el login del resto
auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # compruebo si el metodo es post osea si han dado al boton de enviar
    if request.method == 'POST':
        # recojo lo que ha escrito el usuario en los inputs del form
        username = request.form['username']
        password = request.form['password']
        # uso mi servicio para verificar si el usuario y la clave estan en la base de datos
        user = check_credentials(username, password)
        # si me devuelve un usuario es que todo esta correcto
        if user:
            # esta funcion de flask login es la que crea la cookie de sesion
            login_user(user)
            return redirect(url_for('navigation.home')) 
        # si pone mal la contraseña le salto este mensaje
        flash('Credenciales inválidas')
    # si entra por get simplemente le pinto el html del login
    return render_template('login.html')

@auth_bp.route('/logout')
# le pongo el login required porque no tiene sentido cerrar sesion si no has entrado
@login_required
def logout():
    # esta funcion borra la sesion del usuario actual
    logout_user()
    # cuando termina lo mando otra vez al login
    return redirect(url_for('auth.login'))