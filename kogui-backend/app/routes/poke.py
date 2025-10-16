from flask import Blueprint, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import PokemonCache
from .. import db
import requests
import json

poke_bp = Blueprint('poke', __name__)

@poke_bp.route('/pokemons', methods=['GET'])
@jwt_required()
def list_pokemons():
    """Proxy da listagem da PokéAPI com paginação por limit/offset."""
    from flask import request
    base = current_app.config.get('POKEAPI_BASE', 'https://pokeapi.co/api/v2')
    try:
        limit = int(request.args.get('limit', 30))
        offset = int(request.args.get('offset', 0))
    except ValueError:
        return jsonify({'msg': 'Parâmetros inválidos'}), 400

    url = f"{base}/pokemon?limit={limit}&offset={offset}"
    try:
        resp = requests.get(url, timeout=8)
        data = resp.json()
    except requests.RequestException:
        return jsonify({'msg': 'Erro ao acessar PokéAPI'}), 502

    # opcionalmente poderíamos enriquecer cada item com detalhes
    return jsonify(data), resp.status_code

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
    # attempt to use cached data first
    cache = PokemonCache.query.filter_by(name=name).first()
    if cache:
        try:
            return jsonify(cache.to_dict()), 200
        except Exception:
            # fall through to refetch if cache is corrupt
            pass
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