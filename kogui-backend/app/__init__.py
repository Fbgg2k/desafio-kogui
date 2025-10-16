from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('app.config.Config')

    db.init_app(app)
    jwt.init_app(app)

    # permitir chamadas do frontend durante o desenvolvimento
    # inclui /api, /auth e /users
    CORS(
        app,
        resources={
            r"/api/*": {"origins": "*"},
            r"/auth/*": {"origins": "*"},
            r"/users/*": {"origins": "*"},
        },
        supports_credentials=True,
    )

    from .routes.auth import auth_bp
    from .routes.poke import poke_bp
    from .routes.users import users_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(poke_bp, url_prefix='/api')
    app.register_blueprint(users_bp)

    with app.app_context():
        db.create_all()

    return app