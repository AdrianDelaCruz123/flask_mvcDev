from flask import Flask
from flask_login import LoginManager
from app.extensions import db  

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config['SECRET_KEY'] = 'clave_secreta'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pyhton.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializamos la DB con la app
    db.init_app(app)

    # Configuración de Login
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from app.services.auth_service import get_user
    @login_manager.user_loader
    def load_user(user_id):
        return get_user(user_id)

    from app.controllers import auth_controller, socios_controller, prestamos_controller, navigation_controller, libros_controller, api_controller
    
    app.register_blueprint(navigation_controller.navigation_bp)
    app.register_blueprint(auth_controller.auth_bp)
    app.register_blueprint(socios_controller.socios_bp)
    app.register_blueprint(prestamos_controller.prestamos_bp)
    app.register_blueprint(libros_controller.libros_bp)
    app.register_blueprint(api_controller.api_bp)

    # Crear tablas
    with app.app_context():
        db.create_all()

    return app