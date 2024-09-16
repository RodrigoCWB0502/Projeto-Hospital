from flask import Blueprint, render_template

# Criação do blueprint
notifications_blueprint = Blueprint('notifications', __name__, template_folder='templates')

# Exemplo de rota
@notifications_blueprint.route('/alerts')
def alerts():
    return render_template('alerts.html')
