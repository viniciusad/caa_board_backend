import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS
from flasgger import Swagger

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev-secret-key-aac-mvp'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'aac_board.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Allow CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    login_manager.init_app(app)
    
    app.config['SWAGGER'] = {
        'openapi': '3.0.0',
        'uiversion': 3
    }

    swagger_template = {
        "info": {
            "title": "CAA Board API",
            "description": "API do sistema de Comunicação Alternativa e Ampliada (Cards API).",
            "version": "1.0.0"
        },
        "components": {
            "securitySchemes": {
                "BasicAuth": {
                    "type": "http",
                    "scheme": "basic",
                    "description": "Insira seu usuário e senha cadastrados no banco de dados."
                }
            }
        }
    }
    
    swagger_config = Swagger.DEFAULT_CONFIG.copy()
    swagger_config["specs_route"] = "/api/"
    
    Swagger(app, template=swagger_template, config=swagger_config)

    # Import models here to ensure they are registered with SQLAlchemy
    from app import models

    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)

    with app.app_context():
        db.create_all()

    return app
