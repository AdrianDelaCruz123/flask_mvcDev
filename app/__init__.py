from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager
from app.extensions import db  

def create_app():
    # solo una declaracion de app
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)

    # configuracion de base de datos
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///python.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False 
    
    app.config["SECRET_KEY"] = "dev-secret-key"

    # inicializar la base de datos con la app
    db.init_app(app)

    # configuracion de Login
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from app.services.auth_service import get_user
    @login_manager.user_loader
    def load_user(user_id):
        return get_user(user_id)

    # importar y registrar controladores
    from app.controllers import (
        auth_controller, 
        socios_controller, 
        prestamos_controller, 
        navigation_controller, 
        libros_controller, 
        api_controller
    )
    
    app.register_blueprint(navigation_controller.navigation_bp)
    app.register_blueprint(auth_controller.auth_bp)
    app.register_blueprint(socios_controller.socios_bp)
    app.register_blueprint(prestamos_controller.prestamos_bp)
    app.register_blueprint(libros_controller.libros_bp)
    app.register_blueprint(api_controller.api_bp)

    # crear tablas automaticamente si no existen
    with app.app_context():
        db.create_all()

    return app