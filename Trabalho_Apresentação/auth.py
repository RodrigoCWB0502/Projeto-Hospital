from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, MQTTMessage
from models import Event
from datetime import datetime

auth_blueprint = Blueprint('auth', __name__, template_folder='templates')

@auth_blueprint.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('auth.inicio'))
        else:
            flash('Invalid credentials!')
    return render_template('login.html')

@auth_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth_blueprint.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    if current_user.role != 'Admin':
        flash('Access denied', 'error')
        return redirect(url_for('auth.inicio'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists.', 'error')
            return redirect(url_for('auth.register'))
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, password=hashed_password, role=role)
        db.session.add(new_user)
        db.session.commit()
        flash('User registered successfully!', 'success')
        return redirect(url_for('auth.inicio'))
    return render_template('register.html')

@auth_blueprint.route('/inicio')
@login_required
def inicio():
    return render_template('inicio.html')

@auth_blueprint.route('/sensor')
@login_required
def sensor():
    return render_template('sensor.html')

@auth_blueprint.route('/mqtt')
@login_required
def mqtt():
    if current_user.role not in ['Admin', 'Estático']:
        flash('You do not have access to this page.', 'error')
        return redirect(url_for('auth.inicio'))
    return render_template('mqtt.html')


@auth_blueprint.route('/ligar')
@login_required
def ligar():
    if current_user.role not in ['Admin', 'Operador']:
        flash('You do not have access to this page.', 'error')
        return redirect(url_for('auth.inicio'))
    events = Event.query.order_by(Event.timestamp.desc()).limit(10).all()  # Pega os últimos 10 eventos
    return render_template('ligar.html', events=events)

@auth_blueprint.route('/usuario')
@login_required
def usuario():
    if current_user.role != 'Admin':
        flash('Only admins can access this page.', 'error')
        return redirect(url_for('auth.inicio'))
    users = User.query.all()
    return render_template('usuario.html', users=users)

@auth_blueprint.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if current_user.role != 'Admin':
        flash('Only admins can delete users.', 'error')
        return redirect(url_for('auth.inicio'))
    user_to_delete = User.query.get_or_404(user_id)
    db.session.delete(user_to_delete)
    db.session.commit()
    flash('User deleted successfully.', 'success')
    return redirect(url_for('auth.usuario'))

@auth_blueprint.route('/save_message', methods=['POST'])
def save_message():
    try:
        data = request.get_json()
        if not data or 'message' not in data or 'topic' not in data:
            return jsonify({"status": "error", "message": "Missing message or topic"}), 400

        message = data['message']
        topic = data['topic']
        new_message = MQTTMessage(topic=topic, message=message, timestamp=datetime.utcnow())
        db.session.add(new_message)
        db.session.commit()
        return jsonify({"status": "success", "message": "Message saved"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@auth_blueprint.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        username = request.form['username']
        role = request.form['role']
        user.username = username
        user.role = role
        db.session.commit()
        flash('User updated successfully!', 'success')
        return redirect(url_for('auth.usuario'))
    return render_template('edit_user.html', user=user)

@auth_blueprint.route('/save_event', methods=['POST'])
def save_event():
    data = request.get_json()
    if data and 'event_type' in data:
        new_event = Event(event_type=data['event_type'], timestamp=datetime.utcnow())
        db.session.add(new_event)
        db.session.commit()
        return jsonify({"status": "success", "message": "Event saved"}), 200
    return jsonify({"status": "error", "message": "Missing event type"}), 400