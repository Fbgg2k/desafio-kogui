from flask import Blueprint, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity

# Ajuste o import abaixo conforme a estrutura do seu projeto.
# Ex.: from app.models import User
# O modelo User deve expor: query (SQLAlchemy) ou um método equivalente para buscar pelo id.
try:
    from app.models import User
except Exception:
    # Placeholder mínimo caso não haja um modelo definido ainda.
    class User:
        def __init__(self, id, username, email):
            self.id = id
            self.username = username
            self.email = email

        @staticmethod
        def query_get(pk):
            # Mock: substituir por User.query.get(pk) em produção
            if pk == 1:
                return User(1, "admin", "admin@example.com")
            return None

        # Compatibilidade com SQLAlchemy style: User.query.get(...)
        @staticmethod
        def query():
            class Q:
                @staticmethod
                def get(pk):
                    return User.query_get(pk)
            return Q()

users_bp = Blueprint('users', __name__, url_prefix='/users')


def user_to_dict(user):
    """Serializa um objeto User para JSON com campos seguros."""
    if not user:
        return None
    return {
        "id": getattr(user, "id", None),
        "username": getattr(user, "username", None),
        "email": getattr(user, "email", None),
        # adicione aqui outros campos seguros (evite expor senhas, tokens, etc.)
    }


@users_bp.route('/me', methods=['GET'])
@jwt_required()
def me():
    """
    Retorna os dados do usuário associado ao JWT atual.
    - espera-se que get_jwt_identity() retorne o user_id (ou algo convertível para int).
    - busca o usuário no banco e devolve uma representação segura.
    """
    identity = get_jwt_identity()
    if identity is None:
        return jsonify({'msg': 'Token inválido ou ausente'}), 401

    try:
        user_id = int(identity)
    except (TypeError, ValueError):
        current_app.logger.debug("Identidade do JWT não pôde ser convertida em int: %r", identity)
        return jsonify({'msg': 'Identidade inválida no token'}), 400

    try:
        # Se estiver usando SQLAlchemy: user = User.query.get(user_id)
        user = None
        # tentativa de usar API SQLAlchemy-style
        try:
            user = User.query.get(user_id)
        except Exception:
            # fallback para uma possível API diferente (como o placeholder acima)
            try:
                user = User.query_get(user_id)
            except Exception:
                user = None

        if user is None:
            return jsonify({'msg': 'Usuário não encontrado'}), 404

        return jsonify(user_to_dict(user)), 200

    except Exception as e:
        current_app.logger.exception("Erro ao buscar usuário com id %s: %s", user_id, e)
        return jsonify({'msg': 'Erro interno ao buscar usuário'}), 500