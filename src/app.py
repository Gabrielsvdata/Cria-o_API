#RESPONSÁVEL PELA APLICAÇÃO 

from flask import Flask
from src.controler.colaborador_controller import bp_colaborador

def create_app():
    app = Flask(__name__)
    app.register_blueprint(bp_colaborador)
    return app