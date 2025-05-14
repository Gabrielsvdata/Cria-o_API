# src/app.py

from flask import Flask
from src.controler.colaborador_controller import bp_colaborador
from src.controler.reembolso_controler import bp_reembolso   # ← importe o seu blueprint de reembolsos
from src.model import db
from config import Config
from flasgger import Swagger
from flask_cors import CORS

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
    # registra blueprints
    app.register_blueprint(bp_colaborador)
    app.register_blueprint(bp_reembolso)     # ← registra também o reembolso
    app.config.from_object(Config)

    # CORS configurado para gerar preflight automaticamente em /reembolsos/*
    CORS(
      app, origins=["*"],
      resources={ r"/*": {"origins": "*"} },
      supports_credentials=True,
      methods=["GET","POST","PATCH","DELETE","OPTIONS"],
      allow_headers=["Content-Type","Authorization"]
    )

    db.init_app(app)
    Swagger(app, config=swagger_config)

    with app.app_context():
        db.create_all()

    return app
