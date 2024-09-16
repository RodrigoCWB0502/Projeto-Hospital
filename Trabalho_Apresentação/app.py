from flask import Flask
from flask_login import LoginManager
from auth import auth_blueprint  
from notifications import notifications_blueprint
from models import init_db, db, User
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object('config.Config')
CORS(app)

init_db(app)

login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

app.register_blueprint(auth_blueprint)
app.register_blueprint(notifications_blueprint, url_prefix='/notifications')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Adicione este bloco para criar as tabelas automaticamente
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)