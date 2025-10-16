from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from .. import db
from ..models import User
from sqlalchemy import or_

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    if not (username and email and password):
        return jsonify({'msg': 'Dados ausentes'}), 400
    if User.query.filter(or_(User.username==username, User.email==email)).first():
        return jsonify({'msg': 'Usuário já existe'}), 400
    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'msg': 'Usuário criado'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    email = data.get('email')
    password = data.get('password')
    if not (email and password):
        return jsonify({'msg': 'Dados ausentes'}), 400
    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({'msg': 'Credenciais incorretas'}), 401
    # ensure subject/sub is a string to avoid "Subject must be a string"
    access_token = create_access_token(identity=str(user.id))
    return jsonify({'access_token': access_token})