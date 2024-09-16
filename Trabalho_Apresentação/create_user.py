from werkzeug.security import generate_password_hash
from models import db, User
from app import app

# Dados do usuário que você quer adicionar
username = 'user1'
password = 'password1'
role = 'Admin'

# Hash a senha
hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

# Crie o usuário
new_user = User(username=username, password=hashed_password, role=role)

# Adicione o usuário ao banco de dados
with app.app_context():
    db.session.add(new_user)
    db.session.commit()

print(f'Usuário {username} criado com sucesso.')