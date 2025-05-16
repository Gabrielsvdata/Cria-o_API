# from flask_bcrypt import bcrypt


# def hash_senha(senha):
#     salt = bcrypt.gensalt() 
#     return bcrypt.hashpw(senha.encode('utf-8'), salt).decode('utf-8')

# def checar_senha(senha, senha_hash):
#     return bcrypt.checkpw(senha_hash.encode('utf-8'), senha.encode('utf-8'))

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()  # Instância do Bcrypt para hashing de senhas
def hash_senha(senha):
    
    pw_hash = bcrypt.generate_password_hash(senha)
    return pw_hash.decode("utf-8")


def checar_senha(senha, hash_senha):
    return bcrypt.check_password_hash(hash_senha, senha)

