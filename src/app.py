# RESPONSÁVEL PELA APLICAÇÃO 

from flask import Flask
from src.controler.colaborador_controller import bp_colaborador
from src.controler.reembolso_controler import bp_reembolso
from src.model import db
from config import Config
from flasgger import Swagger
from flask_cors import CORS

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec",           # Nome de referência para a documentação
            "route": "/apispec.json/",      # Rota do JSON usado pelo Swagger UI
            "rule_filter": lambda rule: True,# Todas as rotas serão documentadas
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,                  # Ativa o Swagger UI
    "specs_route": "/apidocs/",          # Rota para acessar o Swagger UI
}

def create_app():
    app = Flask(__name__)               # instancia do Flask

    # 1) Carrega a configuração antes de inicializar extensões
    app.config.from_object(Config)

    # 2) Inicializa extensões que usam a config
    db.init_app(app)                    # inicia a conexão com o banco
    CORS(app, origins=["*"])            # habilita CORS para todas as origens
    Swagger(app, config=swagger_config) # configura o Swagger

    # 3) Registra blueprints (mantendo a estrutura original)
    app.register_blueprint(bp_colaborador)
    app.register_blueprint(bp_reembolso)

    # 4) Cria tabelas caso ainda não existam
    with app.app_context():
        db.create_all()

    return app
