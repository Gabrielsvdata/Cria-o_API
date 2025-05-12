# RESPONSÁVEL PELA APLICAÇÃO 

from flask import Flask
from src.controler.colaborador_controller import bp_colaborador
from src.controler.reembolso_controler import bp_reembolso  # <-- Blueprint do Reembolso adicionado
from src.controler.auth_controler import bp_auth
from src.model import db
from config import Config
from flasgger import Swagger
from flask_cors import CORS
from src.extensions import db, mail
from src.model.password_reset_model import PasswordReset

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec", # <-- Da um nome de referencia para a documentacao
            "route": "/apispec.json/", # <- Rota do arquivo JSON para a construção da documentação
            "rule_filter": lambda rule: True, # <-- Todas as rotas/endpoints serão documentados
            "model_filter": lambda tag: True, # <-- 
        }
    ],
    "static_url_path": "/flasgger_static", 
    "swagger_ui": True, # <-- Ativa a interface do Swagger UI
    "specs_route": "/apidocs/", # <-- Rota para acessar a interface do Swagger UI
}


def create_app():
    app = Flask(__name__) #-- INSTANCIA DO FLASK
    app.register_blueprint(bp_colaborador)
    app.register_blueprint(bp_reembolso)  # <-- Blueprint do Reembolso adicionado
    app.config.from_object(Config)
    app.register_blueprint(bp_auth)


    db.init_app(app) #inicia a conexaõ com o banco de dados 
    mail.init_app(app)
    CORS(app, origins=["*"]) #-- HABILITA O CORS PARA TODAS AS ORIGENS
    Swagger(app, config=swagger_config)

    with app.app_context(): # Se as tabelas não existem, crie
        db.create_all()

    return app
