from werkzeug.security import check_password_hash
from app.models.user import users_db, User

# Función para recuperar usuario por ID 
def get_user(user_id):
    return users_db.get(str(user_id))

# Base de datos de contraseñas 
usuarios_passwords = {
    #Contraseña:admin123
    "admin": "scrypt:32768:8:1$jveT1XZ6bL3mA5at$f1f1b2344819e7365ce2b84484222fff39e3154595f43b3309f34832ed3a8c079e96e25c9fe0ac518473f10a2d7b2d01bcf358a30d68bcc5251e4b102d02b6c2", 
    #Contraseña: 1234
    "usuario": "scrypt:32768:8:1$QfROmZC2ud4Zgg6s$1e6c0fd4f014276184669be3fdf337a2406ca6823f8beea6fe26bbf6e1e82aefff77db7439026ea6e633e784e524196cfaed006a28b5f165cca2d212aa5a0519"
}

def check_credentials(username, password):
    #Verificamos si existe el usuario en la lista de claves
    if username not in usuarios_passwords:
        return None

    # Recuperamos el hash
    hash_guardado = usuarios_passwords[username]

    #Comparamos hash con contraseña plana
    if check_password_hash(hash_guardado, password):
        #Buscamos el objeto usuario real en el modelo
        for user in users_db.values():
            if user.username == username:
                return user
    
    return None