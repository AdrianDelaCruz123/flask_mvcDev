from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, username, role):
        self.id = id
        self.username = username
        self.role = role 

# Aquí guardamos los datos de sesión 
users_db = {
    "1": User("1", "admin", "admin"),
    "2": User("2", "usuario", "user")
}