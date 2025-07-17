from flask import Flask
from src.controler.colaborador_controller import bp_colaborador
from src.controler.reembolso_controler import bp_reembolso
from src.model import db
from config import Config
from flasgger import Swagger
from flask_cors import CORS
from src.controler.ocr_controller import ocr_bp  # Import OK

# Configuração do Swagger
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec",
            "route": "/apispec.json/",
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/",
}

def create_app():
    app = Flask(__name__)

    # 1) Carrega a configuração
    app.config.from_object(Config)

    # 2) Inicializa extensões
    db.init_app(app)
    CORS(app)
    Swagger(app, config=swagger_config)

    # 3) Registra Blueprints
    app.register_blueprint(bp_colaborador)
    app.register_blueprint(bp_reembolso)
    app.register_blueprint(ocr_bp)  # Correto e dentro da função

    # 4) Cria as tabelas
    with app.app_context():
        db.create_all()

    return app
