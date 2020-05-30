from user import User
from werkzeug.security import safe_str_cmp

def autenticate(username, password):
    user = User.find_by_username(username)

    # Si el user es distinto a None lo validamos
    if user and safe_str_cmp(user.password, password):
        # Si las credenciales estan bien retorno el usuario
        return user

def identity(payload):
    user_id = payload['identity']
    return User.find_by_id(user_id)