from flask import Blueprint, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import PokemonCache
from .. import db
import requests
import json

poke_bp = Blueprint('poke', __name__)

@poke_bp.route('/pokemon/<name>', methods=['GET'])
@jwt_required()
def get_pokemon(name):
    # obter identidade do token e converter para int com tratamento
    identity = get_jwt_identity()
    try:
        user_id = int(identity) if identity is not None else None
    except (TypeError, ValueError):
        return jsonify({'msg': 'Identidade inválida no token'}), 400

    # agora pode usar user_id (ex.: log, cache por usuário, ou para marcar favoritos)
    name = name.lower()

    base = current_app.config.get('POKEAPI_BASE', 'https://pokeapi.co/api/v2')
    url = f"{base}/pokemon/{name}"
    try:
        resp = requests.get(url, timeout=6)
    except requests.RequestException:
        return jsonify({'msg': 'Erro ao acessar PokéAPI'}), 502

    if resp.status_code == 200:
        data = resp.json()
        if not cache:
            cache = PokemonCache(name=name, data=json.dumps(data))
            db.session.add(cache)
        else:
            cache.data = json.dumps(data)
        db.session.commit()
        return jsonify(data), 200

    if resp.status_code == 404:
        return jsonify({'msg': 'Pokémon não encontrado'}), 404

    return jsonify({'msg': 'Erro da PokéAPI'}), resp.status_code